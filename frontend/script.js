document.getElementById('upload-form').onsubmit = async function(event) {
    event.preventDefault();
    const formData = new FormData();
    const imageInput = document.querySelector('input[name="image"]');
    const backgroundInput = document.querySelector('input[name="background"]');
    const nameInput = document.querySelector('input[name="name"]');
    const positionInput = document.querySelector('input[name="position"]');
    const trikotnummerInput = document.querySelector('input[name="trikotnummer"]');
    
    formData.append('image', imageInput.files[0]);
    formData.append('background', backgroundInput.files[0]);
    formData.append('name', nameInput.value);
    formData.append('position', positionInput.value);
    formData.append('trikotnummer', trikotnummerInput.value);

    try {
        const response = await fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: formData
        });
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        document.getElementById('result-img').src = url;
    } catch (error) {
        console.error('Error:', error);
    }
};
