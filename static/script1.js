document.addEventListener("DOMContentLoaded", function() {
    // Get the try button
    const tryButton = document.getElementById("try");
    
    // Add event listener to the try button
    tryButton.addEventListener("click", function() {
        // When the button is clicked, trigger a click on the image input
        const imageInput = document.getElementById("imageInput");
        imageInput.click();
    });
  
    // Add event listener to the image input for file change
    document.getElementById('imageInput').addEventListener('change', function(event) {
        // When a file is selected, create a FormData object and append the file to it
        const file = event.target.files[0];
        const formData = new FormData();
        formData.append('image', file);
      
        // Make a POST request to the server with the image data
        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.blob()) // Convert the response to a blob
        .then(result => {
            // Convert the blob to a URL and set it as the source of the result image
            const imageUrl = URL.createObjectURL(result);
            const resultImage = document.getElementById('resultImage');
            resultImage.src = imageUrl;
        })
        .catch(error => console.error('Error:', error)); // Log any errors
        
        // Display the uploaded image
        const uploadedImageUrl = URL.createObjectURL(file);
        const uploadedImage = document.getElementById('uploadedImage');
        uploadedImage.src = uploadedImageUrl;
    });
});