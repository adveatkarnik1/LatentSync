
# **Super-Resolution Enhancement in LipsyncPipeline**

## **🔹 Changes Made for Super-Resolution**
We integrated **GFPGAN/CodeFormer** to enhance face quality in the lip-sync pipeline. The key modifications include:
1. **Extracting faces from the original video** using `affine_transform_video()`.
2. **Computing input-to-output face proportions** to check if super-resolution is required.
3. **Applying GFPGAN/CodeFormer** only when necessary.
4. **Ensuring the final enhanced face is correctly resized before reintegration** into the original video frame.

---

## **🔹 How Face Proportions Are Calculated**
To determine if super-resolution is needed, we compare:
- **Input Face Dimensions (original extracted face before processing)**
- **Output Face Dimensions (restored face from diffusion model)**

We calculate:
```python
res_ratio_h = input_face_h / restored_face_h
res_ratio_w = input_face_w / restored_face_w
```

where:
* `input_face_h, input_face_w` → Height & width of the original detected face.
* `restored_face_h, restored_face_w` → Height & width of the generated face.

**🔹 How We Check If Super-Resolution Is Needed**
* If `res_ratio_h > 1.0` or `res_ratio_w > 1.0`, the restored face is smaller than the original face, so **we apply super-resolution**.
* **If the restored face is already the same size or larger**, we **skip super-resolution**.

**✅ Decision Table**
| Case | Input Face | Restored Face | Resolution Ratio | Apply Super-Resolution? |
|------|------------|---------------|------------------|----------------------|
| **Low-Res Output** | `256×256` | `128×128` | `2.0` | ✅ Yes |
| **Same-Size Output** | `256×256` | `256×256` | `1.0` | ❌ No |
| **Larger Output** | `256×256` | `512×512` | `0.5` | ❌ No |

**🔹 How We Apply Super-Resolution**
If needed, we apply **GFPGAN or CodeFormer**, then ensure the face is correctly resized:

```python
if res_ratio_h > 1.0 or res_ratio_w > 1.0:
    print(f"Applying super-resolution on face {i}...")
    
    if superres.lower() == "gfpgan":
        restored_face = self.gfpgan_enhance(restored_face)
    elif superres.lower() == "codeformer":
        restored_face = self.codeformer_enhance(restored_face)

    # Ensure restored face matches input face size
    restored_face_h, restored_face_w = restored_face.shape[:2]
    if restored_face_h != input_face_h or restored_face_w != input_face_w:
        print("Resizing restored face to match input face size...")
        restored_face = cv2.resize(restored_face, (input_face_w, input_face_h), interpolation=cv2.INTER_LANCZOS4)
```

* **Ensures that even after super-resolution, the face is correctly resized.**
* **Prevents unwanted distortions when pasting the face back into the original video.**

**🔹 How We Reintegrate the Enhanced Face into the Video**
Once enhanced, we **paste the restored face back into the original frame**:

```python
x1, y1, x2, y2 = boxes[i]
restored_face_resized = cv2.resize(restored_face, (x2 - x1, y2 - y1), interpolation=cv2.INTER_LANCZOS4)
original_frame[y1:y2, x1:x2] = restored_face_resized  # Paste enhanced face back
```

* Uses **bounding box coordinates** to locate the face in the full frame.
* Ensures **only the face is modified**, while the **background remains unchanged**.

**✅ Summary of Enhancements**
✔ **Identifies if super-resolution is needed based on input-to-output face proportions.**
✔ **Applies GFPGAN/CodeFormer only when the restored face is lower resolution.**
✔ **Ensures the enhanced face matches the correct size before reintegration.**
✔ **Replaces only the face in the video, keeping the rest of the frame untouched.**

🚀 **Now, the lip-sync pipeline produces high-quality, sharp faces with accurate lip movements!**
