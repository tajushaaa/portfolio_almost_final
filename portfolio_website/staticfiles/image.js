function AdImage() {
  document.addEventListener("DOMContentLoaded", () => {
    const addImageBtn = document.getElementById("add-additional-image");
    const formsetContainer = document.getElementById("additional-image-formset");

    let formsetCount = formsetContainer.querySelectorAll(".image-form").length;

    addImageBtn.addEventListener("click", () => {
      const formset = document.createElement("div");
      formset.className = "image-form";
      formset.innerHTML = `
        <label for="id_additionalimage_set-${formsetCount}-image">Additional images:</label>
        <input type="file" name="additionalimage_set-${formsetCount}-image" id="id_additionalimage_set-${formsetCount}-image" accept="image/*">
      `;
      formsetContainer.appendChild(formset);
      formsetCount++;
    });
  });
}
AdImage();
