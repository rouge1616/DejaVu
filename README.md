# DejaVu: Intra-operative simulation for surgical gesture rehearsal
Official code and data for realistic intraoperative physics-based simulations for surgery

<p align="center">
  <img src="assets/liver1.gif" width="45%" />
  <img src="assets/liver2.gif" width="46.5%" />
</p>

## Description

**DejaVu** is a surgical simulation tool for intra-operative gesture rehearsal based on the SOFA framework. It bridges pre-op simulation and intra-op augmented reality by using real-time physical modeling and intra-operative images to deliver visually accurate, interactive organ simulations for grasping, pulling, and cutting.

It has also been successfully used for generating training data for deep learning models and as ground-truth to validate elastic registration or 3D reconstruction methods

[Read the Paper](https://hal.science/hal-01542395/document)  and [Watch the Explainer Video](https://www.youtube.com/watch?v=-UJYWlaTZr0)



## Installation of SOFA

To install the SOFA framework, follow the [official installation guide](https://www.sofa-framework.org/download/) for instructions tailored to your OS.
The scenes are plugin-free and use SOFA core modules, so you should be good to go.


## Citation

If you use this software, please cite the following paper:

**Haouchine, N., Stoyanov, D., Roy, F. and Cotin, S.**  
Dejavu: Intra-operative simulation for surgical gesture rehearsal. In MICCAI 2017, Proceedings, Part II 20 (pp. 523-531).

### BibTeX

```bibtex
@inproceedings{haouchine2017dejavu,
  title={Dejavu: Intra-operative simulation for surgical gesture rehearsal},
  author={Haouchine, Nazim and Stoyanov, Danail and Roy, Frederick and Cotin, Stephane},
  booktitle={Medical Image Computing and Computer-Assisted Intervention- MICCAI 2017: 20th International Conference, Quebec City, QC, Canada, September 11-13, 2017, Proceedings, Part II 20},
  pages={523--531},
  year={2017},
  organization={Springer}
}
```
---

## Examples

### 🧠 1. Brain Deformation Simulation  
![Brain Deformation](gifs/brain_deform.gif)  
Simulates intraoperative brain shift during tumor resection using patient-specific MRI-derived meshes and FEM-based deformation.


### 🔪 2. Liver Cutting  
![Liver Cutting](gifs/liver_cut.gif)  
A soft tissue liver model that allows simulated surgical cutting with dynamic response and mesh splitting.


### 🪛 3. Tool-Tissue Interaction  
![Tool-Tissue Interaction](gifs/tool_tissue.gif)  
Interactive manipulation of tissue using a virtual probe, with contact forces and tissue feedback.

### 🎯 4. Needle Insertion  
![Needle Insertion](gifs/needle_insertion.gif)  
Demonstrates accurate needle trajectory modeling through multilayer tissue, including puncture mechanics.

### 📊 5. Multimodal Registration Viewer  
![Multimodal Viewer](gifs/multimodal_viewer.gif)  
Visualizes and validates registration between simulated anatomy and imaging data (e.g., preop MRI and intraop ultrasound).

