const fileSelect = document.getElementById("fileSelect"),
  fileElem = document.getElementById("file"),
  fileList = document.getElementById("fileList"),
  fileListNumb = document.getElementById("fileListNumb"),
  showMediaBtn = document.getElementById("showMediaBtn"),
  box = document.getElementById("box"),
  spinner = document.getElementById("spinner"),
  buttonText = document.getElementById("buttonText"),
  submitBtn = document.getElementById("submitBtn");

fileSelect.addEventListener(
  "click",
  function (e) {
    if (fileElem) {
      fileElem.click();
    }
    e.preventDefault(); // prevent navigation to "#"
  },
  false
);

function loading(){
  // Show Spinner and Uploading Text
  spinner.classList.remove("d-none");
  buttonText.innerHTML = " Uploading...";
  submitBtn.disabled = true;
}

/* events fired on the drop targets */
box.addEventListener("dragover", function( event ) {
  box.classList.add("box-is-active");
  // prevent default to allow drop
  event.preventDefault();
}, false);
box.addEventListener("dragleave", function( event ) {
  box.classList.remove("box-is-active");
  // prevent default to allow drop
  event.preventDefault();
}, false);
box.addEventListener("drop ", function( event ) {
  console.log("dropped")
  box.classList.remove("box-is-active");
  // prevent default to allow drop
  event.preventDefault();
}, false);

fileElem.addEventListener("change", handleFiles, false);

function handleFiles() {
  if (!this.files.length) {
    fileList.innerHTML = "<p>Keine Bilder ausgewählt!</p>";
  } else {
    fileList.innerHTML = "";
    showMediaBtn.innerHTML = "";

    var fileNumb = 0;
    const list = document.createElement("ul");
    list.classList.add("p-0");
    fileList.appendChild(list);
    for (let i = 0; i < this.files.length; i++) {
      const li = document.createElement("li");
      list.appendChild(li);

      const fileSize = this.files[i].size / 1000;
      let fileSizeRounded = Math.round(fileSize) + "KB";
      if (fileSize > 1000) {
        var numb = fileSize / 1000;
        fileSizeRounded = Math.round((numb + Number.EPSILON) * 100) / 100 + "MB";
      }

      let fileName = this.files[i].name;
      if (fileName.length >= 12) {
        let splitName = fileName.split(".");
        fileName = splitName[0].substring(0, 12) + "... ." + splitName[1];
      }

      const img = document.createElement("img");
      img.src = URL.createObjectURL(this.files[i]);
      img.width = 60;
      img.classList.add("obj");
      img.classList.add("py-1");
      img.onload = function () {
        URL.revokeObjectURL(this.src);
      };
      li.appendChild(img);
      const info = document.createElement("span");
      info.classList.add("text");
      info.innerHTML = " " + fileName + " " + fileSizeRounded;
      li.appendChild(info);
      // Increase Media Number by 1
      fileNumb++;
    }
    showMediaBtn.innerHTML = fileNumb + " Medien anzeigen";
    showMediaBtn.classList.add("show")
  }
}