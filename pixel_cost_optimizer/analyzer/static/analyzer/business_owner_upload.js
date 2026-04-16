function showFileInfo(input) {
    const fileInfo = document.getElementById('file-info');
    const uploadBtn = document.getElementById('upload-btn');
    if (input.files && input.files[0]) {
        const file = input.files[0];
        fileInfo.style.display = 'block';
        fileInfo.innerHTML = `<strong>Selected File:</strong> ${file.name} (${(file.size/1024/1024).toFixed(2)} MB)`;
        uploadBtn.disabled = false;
    } else {
        fileInfo.style.display = 'none';
        fileInfo.innerHTML = '';
        uploadBtn.disabled = true;
    }
}
