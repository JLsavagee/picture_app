// Page2.js
import React from 'react';
import Sidebar from '../components/sidebar';
import "./css/Automatic.css";

const Page2 = () => {
    return (
        <div className="automatic-page">
            <Sidebar />
            <h1>This is Page "automatic"</h1>
            <div className="automatic-content">
                <div className="folderId-field">
                    <h1>Folder-ID</h1>
                </div>
                <div className="background-upload">
                    <h1>Background Upload</h1>
                </div>
                <div className='list-preview'>
                    <h1>List-preview</h1>
                </div>
                <div className="auto-create-button">
                    <button>Create</button>
                </div>
            </div>
        </div>
    )
}

export default Page2;
