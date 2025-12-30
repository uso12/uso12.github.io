**Markdown**

# Photography Website Update Workflow

This guide documents the steps to add new photos, update the gallery, and deploy changes to GitHub.

## 0. Prerequisites
Ensure you have the required Python libraries installed:
```bash
pip install Pillow
```

---

## 1. Import New Photos

1. Select your **raw/high-res** photos (e.g., from your camera export).
2. Copy them into the **`new-full-added`** folder.
   * *Note: Do not worry about file size or rotation; the script handles this.*

## 2. Process Images

Run the organization script to optimize images and prepare them for the web.

**Bash**

```
python organize_photos.py
```

**What this does:**

* Auto-rotates images based on EXIF data.
* Creates optimized low-res thumbnails in `photos-reduce`.
* Creates web-optimized full-res versions (under 10MB) in `photos-1_5_resolution`.
* Moves the original raw files to `new-full-added/old` (archives them).

---

## 3. Register Images (The JSON Step)

Open **`images.json`** in your code editor. You must tell the website which category the new photos belong to.

1. Find the filenames of your new photos (look in `photos-reduce` if you forgot them).
2. Add the filenames to the appropriate list:
   * **`base`** : Images shown immediately on the page load.
   * **`additional`** : Images hidden behind the "View More" button.

**Example:**

**JSON**

```
"street": {
    "base": [
        "EXISTING_PHOTO.jpg",
        "NEW_PHOTO_1.jpg"   <-- Add comma after previous item!
    ],
    ...
}
```

---

## 4. Finalize Organization & Build

Now that the JSON is updated, run the scripts again to sort the files and generate the HTML.

1. **Sort Files:** Move the new images into their subfolders (Street/Nature/Portrait).
   **Bash**

   ```
   python organize_photos.py
   ```
2. **Build Website:** Generate the new `index.html`.
   **Bash**

   ```
   python generate_site_new.py
   ```

---

## 5. Deploy to GitHub

Push your changes to the live website.

**Bash**

```
# 1. Add changes (automatically ignores raw files in new-full-added)
git add .

# 2. Save snapshot
git commit -m "Added new photos to street gallery"

# 3. Push to GitHub
git push origin main
```

---

## Troubleshooting

### "File too large" / 50MB Error

* **Cause:** You accidentally tried to upload raw images from `new-full-added`.
* **Fix:** Ensure your `.gitignore` file includes `new-full-added/`. Then run:
  **Bash**

  ```
  git reset
  git add .
  git commit -m "Fix large files"
  git push
  ```

### "Fetch First" / Rejected Updates

* **Cause:** The version on GitHub is different from your computer (sync conflict).
* **Fix:** Since your computer has the master copy of the photos, force the update:
  **Bash**

  ```
  git push origin main --force
  ```

### Images are Sideways

* **Cause:** The EXIF rotation tag was missing.
* **Fix:** The updated script uses `ImageOps.exif_transpose`. Delete the sideways version from `photos-reduce` and re-run the process with the original file.
