# Put the profile on GitHub

1. Unzip `github-profile.zip`.
2. Copy its `README.md` and `assets` folder into the root of your `NathanHor22/NathanHor22` profile repository. Keep that folder structure so the images resolve.
3. Preview the README in GitHub, then commit when you are happy with it.

The profile uses ordinary Markdown, images, links and expandable sections. Each roster card opens a repository. The selected Digimon feature is a looping GIF; selecting a card does not dynamically change it.

## Your animation

- `assets/digimon-select.gif`: 1200 × 660, 72 frames, a six-second loop, approximately 2.5 MiB.
- `assets/digimon-still.png`: static version, also linked below the animation in the README.
- `model/digimon-concept.blend`: editable Blender 5.0 scene, including the 3D model, materials, lights, camera and rotation.
- `model/build_digimon.py`: procedural source for rebuilding the model and rendering its turntable.

The enclosure is an original visual concept for this portfolio. The mint face and three-button interaction come from the Digimon firmware. The housing dimensions, carry loop, button arrangement and exterior details are a design study, not measured or fabrication-ready CAD. The animation does not demonstrate a verified live ChatGPT dot connection.

To use future footage or a new turntable, replace `assets/digimon-select.gif` while keeping the filename. Update `assets/digimon-still.png` too. For a standalone project GIF instead of this whole selection panel, update the README image path to that file.

## Editable source

The separate `design-source.zip` contains the Blender scene, its builder script, the vector assets and the animation assembly scripts. The README upload bundle only contains files needed to display the profile.

The SVGs use system fonts and contain their own colours, so the panels retain their appearance on light and dark GitHub themes. All artwork is original; the visual direction borrows comic-panel and character-roster conventions without using Marvel branding.
