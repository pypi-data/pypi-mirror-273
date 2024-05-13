"""
Code for warping a 2D mesh.
"""

import cv2 
import torch
import torch.nn as nn
from scipy.spatial import Delaunay
import numpy as np

from pytorch3d.renderer.mesh.rasterizer import Fragments

from toon3d.warp.tri_rasterize import rasterize_face_verts, rasterize_texture


def get_simplices(points):
    tri = Delaunay(points.detach().cpu().numpy())
    simplices = torch.tensor(tri.simplices, device=points.device)
    return simplices

def get_half_edges(faces):
    half_edges = torch.stack((faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]), dim=0).permute(1, 0, 2).flatten(0, 1)
    return half_edges

def get_edge_twins(half_edges, edge_pairs=None):
    if edge_pairs is None:
        edge_pairs = get_edge_pairs(half_edges)

    twins = torch.full((len(half_edges),), -1).to(half_edges.device)
    twins[edge_pairs[0]] = edge_pairs[1]
    twins[edge_pairs[1]] = edge_pairs[0]

    return twins

def get_edge_pairs(half_edges):
    unique, occurances = torch.unique(half_edges.sort().values, dim=0, return_inverse=True)
    expanded_occurances = occurances[...,None].expand(-1, len(occurances))
    matches = expanded_occurances == expanded_occurances.T

    diagonal = torch.eye(len(matches), dtype=torch.bool) # don't let it match to itself
    matches[diagonal] = False

    edge_pairs = matches.nonzero().T
    return edge_pairs

### drawing utils

def draw_tris(mesh, image=None, points=None, color=None, thickness=1):

    edges = mesh.half_edges.sort(1).values.unique(dim=0)
    if points is None:
        points = mesh.points

    edge_points = points[edges]

    if color is None:
        color = (0, 0, 0)

    if image is None:
        image = mesh.image[0].cpu().numpy()

    image = image.copy()

    for edge_point in edge_points:
        x1, y1, x2, y2 = edge_point.flatten().int()
        x1, y1, x2, y2 = x1.item(), y1.item(), x2.item(), y2.item()
        image = cv2.line(image, (x1, y1), (x2, y2), color, thickness=thickness, lineType=cv2.LINE_AA)
    
    return image

def draw_points(mesh, image=None, points=None, colors=None):

    if image is None:
        image = mesh.image[0].cpu().numpy()

    image = image.copy()
    
    if colors is None:
        colors = [(1.0, 0, 0) * len(points)]

    for point, color in zip(points, colors):
        x, y = point[0].int().item(), point[1].int().item()
        image = cv2.circle(image, (x, y), 2, color, thickness=5)
    return image

class FrameMeshes(nn.Module):
    def __init__(self, corr_points_padded, corr_masks_padded, depths, heights, widths):
        super().__init__()

        self.n = len(corr_points_padded)

        self.corr_points_padded = corr_points_padded.clone().float()
        self.corr_masks_padded = corr_masks_padded.clone()

        # make lists
        self.corr_points_list = [pts[pts_mask] for pts, pts_mask in zip(corr_points_padded, corr_masks_padded)]
        self.simplices_list = []

        for ndx in range(self.n):

            corr_points = self.corr_points_list[ndx]

            simplices = get_simplices(corr_points)
            self.simplices_list.append(simplices)

        self.points_list = []
        for corr_points in self.corr_points_list:
            self.points_list.append(corr_points)

        # num coords
        self.num_corrs_per_mesh = [len(cp) for cp in self.corr_points_list]
        self.num_points_per_mesh = [len(p) for p in self.points_list]

        # packed 
        self.corr_points_packed = torch.cat(self.corr_points_list)
        self.points_packed = torch.cat(self.points_list)

        # zs
        self.corr_zs_list = [depths[ndx][self.corr_points_list[ndx][...,1].int(), self.corr_points_list[ndx][...,0].int()] for ndx in range(self.n)]
        self.zs_list = []
        for corr_zs in self.corr_zs_list:
            self.zs_list.append(corr_zs)

        self.corr_zs_padded = torch.stack([depths[ndx][self.corr_points_padded[ndx,...,1].int(), self.corr_points_padded[ndx,...,0].int()] for ndx in range(self.n)])
        self.corr_zs_packed = self.corr_zs_padded[self.corr_masks_padded]
        self.zs_packed = torch.cat(self.zs_list)

        # deltas
        self.delta_corr_points_padded = nn.Parameter(torch.zeros_like(self.corr_points_padded))
        self.delta_corr_zs_padded = nn.Parameter(torch.zeros_like(self.corr_zs_padded))

        # pack simplices
        simplices_shifts = torch.cat([torch.tensor([0]), torch.tensor(self.num_points_per_mesh).cumsum(0)[:-1]])
        self.simplices_shifted_list = [simplices + shift for simplices, shift in zip(self.simplices_list, simplices_shifts)]
        self.simplices_packed = torch.cat(self.simplices_shifted_list)

        # import pdb; pdb.set_trace()


    ### delta points ###
        
    @property
    def delta_corr_points_packed(self):
        return self.delta_corr_points_padded[self.corr_masks_padded]

    ### warped points ###
    
    #packed
    @property
    def warped_corr_points_packed(self):
        return self.corr_points_packed + self.delta_corr_points_packed
    
    @property
    def warped_points_packed(self):
        return torch.cat(self.warped_points_list)
    
    # padded
    @property
    def warped_corr_points_padded(self):
        return self.corr_points_padded + self.delta_corr_points_padded
    
    # list
    @property
    def warped_corr_points_list(self):
        return self.warped_corr_points_packed.split(self.num_corrs_per_mesh)
    
    @property
    def warped_points_list(self):
        warped_points_list = []
        for warped_corr_points in self.warped_corr_points_list:
            warped_points_list.append(warped_corr_points)

        return warped_points_list
    
    ### delta zs ###

    # packed
    @property
    def delta_corr_zs_packed(self):
        return self.delta_corr_zs_padded[self.corr_masks_padded]
    
    @property
    def delta_zs_packed(self):
        return torch.cat(self.delta_zs_list)

    # list
    @property
    def delta_corr_zs_list(self):
        return self.delta_corr_zs_packed.split(self.num_corrs_per_mesh)
    
    @property
    def delta_zs_list(self):
        delta_zs_list = []
        for delta_corr_zs in self.delta_corr_zs_list:
            delta_zs_list.append(delta_corr_zs)

        return delta_zs_list
    
    ### warped zs ###

    # padded
    @property
    def warped_corr_zs_padded(self):
        return self.corr_zs_padded + self.delta_corr_zs_padded
    
    # packed
    @property
    def warped_zs_packed(self):
        return self.zs_packed + self.delta_zs_packed

    # list
    @property
    def warped_corr_zs_list(self):
        return (self.corr_zs_packed + self.delta_corr_zs_packed).split(self.num_corrs_per_mesh)
    
    @property
    def warped_zs_list(self):
        return self.warped_zs_packed.split(self.num_points_per_mesh)
    


class WarpMesh(nn.Module):
    def __init__(self, points, simplices, height, width, uv_points=None, device="cpu"):
        """
        Creates a Mesh designed to fit an input image with triangulation
        """
        super().__init__()

        self.height = height
        self.width = width

        self.points = points.to(device).float()
        self.faces = simplices.to(device)

        if uv_points is None:
            uv_points = self.points.clone()
        self.uv_points = uv_points.to(device)

        self.half_edges = get_half_edges(self.faces)
        self.edge_pairs = get_edge_pairs(self.half_edges)
        self.edge_twins = get_edge_twins(self.half_edges, self.edge_pairs)

        self.device = device

        self.dpx = 1 / min(self.height - 1, self.width - 1)
        self.faces_per_pixel = 1

        self.z_offset = 1
        self.pzs = None

    @property
    def normalized_points(self):
        points = self.points
        points_normed = points / torch.tensor([self.width - 1, self.height - 1], device=self.device) * 2 - 1
        ratio = self.width / self.height

        if ratio > 1:
            points_normed[..., 0] *= ratio
        elif ratio < 1:
            points_normed[..., 1] /= ratio

        points_normed[..., 0] *= (self.width - 1) / self.width
        points_normed[..., 1] *= (self.height - 1) / self.height

        return points_normed # exact barycentric

    @property
    def verts(self):
        points_normed = self.normalized_points
        zs = torch.full([len(points_normed),], self.z_offset).float().to(self.device)
        if self.pzs is not None:
            zs += self.pzs.to(self.device)
        verts = torch.cat([points_normed, zs[...,None]], 1)
        # zs = torch.ones(len(points_normed), 1).to(self.device)
        # verts = torch.cat([points_normed, zs], 1)

        return verts

    @property
    def face_verts(self):
        return self.verts[self.faces]
    
    @property
    def verts_uvs(self):
        uv_points_normed = self.uv_points / torch.tensor([self.width - 1, self.height - 1], device=self.device)
        return uv_points_normed[self.faces]

    def rasterize(self, variations=False):
        face_verts = self.face_verts.clone()

        # make variations
        if variations:
            face_verts = torch.cat([face_verts, self.face_verts_variations])

        # rasterize
        while True:
            fragments = rasterize_face_verts(face_verts, (self.height, self.width), self.faces_per_pixel)
            
            # want to make sure there are enough k-dims in rasterization for all faces
            # if torch.any(fragments.pix_to_face[...,-1] > -1):
            #     self.faces_per_pixel += 1
            # else:
            return fragments

    def render(self, image, fragments=None):
        if len(image.shape) == 2:
            image = image[None,...,None]
        if len(image.shape) == 3:
            image = image[None]

        assert image.shape[1] == self.height and image.shape[2] == self.width
        assert len(image.shape) == 4, "must be of size (1, height, width, c)"
        if fragments is None:
            fragments = self.rasterize()

        rendered_image = rasterize_texture(image, self.verts_uvs, fragments)[0]

        return rendered_image