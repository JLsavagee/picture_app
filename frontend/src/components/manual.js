// Page1.js
import React from 'react';
import Sidebar from '../components/sidebar';
import "./css/Manual.css";

const Page1 = () => {
    return (
        <div className="manual-page">
            <Sidebar />
            <h1>This is Page "manual"</h1>
            <div className="manual-content">
                <div className="name-field">
                    <h1>Name</h1>
                </div>
                <div className="surname-field">
                    <h1>Nachname</h1>
                </div>
                <div className="position-field">
                    <h1>Position</h1>
                </div>
                <div className='image-container'>
                    <div className='image-upload'>
                        <h1>Image</h1>
                    </div>
                    <div className='background-upload'>
                        <h1>Background</h1>
                    </div>
                </div>
                <div className="manual-create-button">
                    <button>Create</button>
                </div>
            </div>
        </div>
    )
}

export default Page1;
