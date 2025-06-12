# DejaVu
Code and data for realistic intraoperative physics-based simulations for surgery

## Description

**DejaVu** is a surgical simulation framework built on the SOFA (Simulation Open Framework Architecture) platform. It enables high-fidelity, real-time simulation of patient-specific anatomies and surgical scenarios. Designed for researchers, clinicians, and educators, it supports deformable tissue modeling, interactive tool dynamics, and integration with medical imaging data.

- Real-time interaction and collision response  
- Supports soft tissue cutting and deformation  
- Integrates seamlessly with MRI/CT imaging  
- Easily extensible with custom plugins and scenes  

📄 [Read the Paper](https://arxiv.org/abs/2401.12345)  
🎥 [Watch the Demo](https://youtu.be/demo-video-link)

![Software Overview](images/overview.png)

---

## Installation of SOFA

To install the SOFA framework, follow the [official installation guide](https://www.sofa-framework.org/download/) for instructions tailored to your OS.

The scenes are plugin-free and use SOFA core modules, so you should be good to go.

---


## Citation

If you use this software, please cite the following paper:

**Doe J., Smith A., Rouge N.**  
*RealSim: Real-Time Biomechanical Simulation for Surgical Planning Using SOFA*.  
arXiv preprint arXiv:2401.12345, 2024.

### BibTeX

```bibtex
@article{doe2024realsim,
  title={RealSim: Real-Time Biomechanical Simulation for Surgical Planning Using SOFA},
  author={Doe, John and Smith, Alice and Rouge, Nazeem},
  journal={arXiv preprint arXiv:2401.12345},
  year={2024}
}
```
---

## Examples

### 🧠 1. Brain Deformation Simulation  
![Brain Deformation](gifs/brain_deform.gif)  
Simulates intraoperative brain shift during tumor resection using patient-specific MRI-derived meshes and FEM-based deformation.

---

### 🔪 2. Liver Cutting  
![Liver Cutting](gifs/liver_cut.gif)  
A soft tissue liver model that allows simulated surgical cutting with dynamic response and mesh splitting.

---

### 🪛 3. Tool-Tissue Interaction  
![Tool-Tissue Interaction](gifs/tool_tissue.gif)  
Interactive manipulation of tissue using a virtual probe, with contact forces and tissue feedback.

---

### 🎯 4. Needle Insertion  
![Needle Insertion](gifs/needle_insertion.gif)  
Demonstrates accurate needle trajectory modeling through multilayer tissue, including puncture mechanics.

### 📊 5. Multimodal Registration Viewer  
![Multimodal Viewer](gifs/multimodal_viewer.gif)  
Visualizes and validates registration between simulated anatomy and imaging data (e.g., preop MRI and intraop ultrasound).

