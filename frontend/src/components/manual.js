import React, { useState } from 'react';
import Sidebar from '../components/sidebar';
import "./css/Manual.css";

const Manual = () => {
    const [imagePreview, setImagePreview] = useState(null);
    const [backgroundPreview, setBackgroundPreview] = useState(null);

    const handleImageChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setImagePreview(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleBackgroundChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setBackgroundPreview(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        
        const formData = new FormData(event.target);

        // Log all form data before submission 
        console.log("Form data before submission:");
        for (let [key, value] of formData.entries()) {
            console.log(`${key}: ${value}`);
        }

        try {
            const response = await fetch('http://127.0.0.1:5000/upload/manual', {
                method: 'POST',
                body: formData
            });
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className="manual-page">
            <Sidebar />
            <h1>This is Page "manual"</h1>
            <div className="manual-content">
                <form id="manual-upload-form" onSubmit={handleSubmit} encType="multipart/form-data">
                    <div className="name-field">
                        <p>Name</p>
                        <input type="text" name="name" placeholder="Name" /> 
                    </div>
                    <div className="surname-field">
                        <p>Nachname</p>
                        <input type="text" name="surname" placeholder="Surname" />
                    </div>
                    <div className="position-field">
                        <p>Position</p>
                        <select name="position">
                            <option value="" disabled selected>Position</option>
                            <option value="MITTELFELD">MITTELFELD</option>
                            <option value="ABWEHR">Abwehr</option>
                            <option value="ANGRIFF">Angriff</option>
                            <option value="TORWART">Torwart</option>
                            <option value="TRAINER">Trainer</option>
                        </select>
                    </div>
                    <div className='image-container'>
                        <div className='image-upload'>
                            <input type="file" name="image" accept="image/*" onChange={handleImageChange} />
                            {imagePreview ? (
                                <img src={imagePreview} alt="Image Preview" className="image-preview" />
                            ) : (
                                <div className="image-placeholder-box">Image Preview</div> // Placeholder for image
                            )}
                        </div>
                        <div className='background-upload'>
                            <input type="file" name="background" accept="image/*" required onChange={handleBackgroundChange} />
                            {backgroundPreview ? (
                                <img src={backgroundPreview} alt="Background Preview" className="image-preview" />
                            ) : (
                                <div className="image-placeholder-box">Background Preview</div> // Placeholder for background
                            )}
                        </div>
                    </div>
                    <div className="manual-create-button">
                        <button type="submit">Create</button>
                    </div>
                </form>
            </div>
        </div>
    )
}

export default Manual;
