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
                <form id="manual-upload-form" enctype="multipart/form-data">
                    <div className="name-field">
                        <input type="text" name="name" placeholder="Name" /> 
                    </div>
                    <div className="surname-field">
                        <input type="text" name="surname" placeholder="Surname" />
                    </div>
                    <div className="position-field">
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
                            <h1>Image</h1>
                        </div>
                        <div className='background-upload'>
                            <h1>Background</h1>
                        </div>
                    </div>
                    <div className="manual-create-button">
                        <button>Create</button>
                    </div>
                </form>
            </div>
        </div>
    )
}

export default Page1;
