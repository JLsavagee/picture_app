// Page2.js
import React, { useState } from 'react';
import Sidebar from '../components/sidebar';
import "./css/Automatic.css";

const Page2 = () => {
    const [backgroundPreview, setBackgroundPreview] = useState(null);

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
            const response = await fetch('http://127.0.0.1:5000/upload', {
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
        <div className="automatic-page">
            <Sidebar />
            <h1>This is Page "automatic"</h1>
            <div className="automatic-content">
                <form id="automatic-upload-form" onSubmit={handleSubmit} encType="multipart/form-data">
                    <div className="folderId-field">
                        <p>Folder-ID</p>
                        <input type="text" name="folder-id" placeholder="insert folder-id" value="10TZJod3vKArx0XBPf6XLIcultMxtj-87" />
                    </div>
                    <div className="auto-background-upload">
                        <p>Background Upload</p>
                        <input type="file" name="background" accept="image/*" required onChange={handleBackgroundChange} />
                                {backgroundPreview ? (
                                    <img src={backgroundPreview} alt="Background Preview" className="auto-image-preview" />
                                ) : (
                                    <div className="image-placeholder-box">Background Preview</div> // Placeholder for background
                                )}
                    </div>
                    <div className='list-preview'>
                        <p>List-preview</p>
                        <input type="file" name="background" accept="image/*" />
                        <div className="placeholder-box">Name-List Preview</div>
                    </div>
                    <div className="auto-create-button">
                        <button type="submit">Generate</button>
                    </div>
                </form>    
            </div>
        </div>
    )
}

export default Page2;
