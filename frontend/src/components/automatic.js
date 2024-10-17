import React, { useState } from 'react';
import * as XLSX from 'xlsx';
import Sidebar from '../components/sidebar';
import "./css/Automatic.css";

const Automatic = () => {
    const [backgroundPreview, setBackgroundPreview] = useState(null);
    const [nameListData, setNameListData] = useState([]);
    const [processing, setProcessing] = useState(false);

    const API_URL = process.env.REACT_APP_API_URL;

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

    const handleNameListChange = (event) => {
        const file = event.target.files[0];
        if (file) {
          const fileExtension = file.name.split('.').pop().toLowerCase();
      
          if (fileExtension === 'csv') {
            handleCSV(file);
          } else if (fileExtension === 'xlsx' || fileExtension === 'xls') {
            handleXLSX(file);
          } else {
            alert('Unsupported file type!');
          }
        }
      };
      
      const handleCSV = (file) => {
        const reader = new FileReader();
        reader.onload = (e) => {
          const text = e.target.result;
          const lines = text.split('\n').map(line => line.split(','));
          setNameListData(lines);
        };
        reader.readAsText(file);
      };

      const handleXLSX = (file) => {
        const reader = new FileReader();
        reader.onload = (e) => {
          const data = new Uint8Array(e.target.result);
          const workbook = XLSX.read(data, { type: 'array' });
          const firstSheetName = workbook.SheetNames[0];
          const worksheet = workbook.Sheets[firstSheetName];
          const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
          setNameListData(jsonData);
        };
        reader.readAsArrayBuffer(file);
      };      

    const handleSubmit = async (event) => {
        event.preventDefault();
        
        const formData = new FormData(event.target);

        try {
            setProcessing(true);
            const response = await fetch(`${API_URL}/upload/automatic`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }

            // Start polling for status after submission
            pollForProcessingStatus();
            
        } catch (error) {
            console.error('Error:', error);
            setProcessing(false); // Reset processing state in case of error
        }
    };

    const pollForProcessingStatus = async () => {
        const pollInterval = 5000; // Poll every 5 seconds

        const checkProcessingStatus = async () => {
            try {
                const response = await fetch(`${API_URL}/check_processing_status`);
                const data = await response.json();

                if (data.status === 'completed') {
                    // Trigger ZIP download
                    window.location.href = `${API_URL}/download_zip`;
                    setProcessing(false); // Processing is done
                } else {
                    // Keep polling if processing is still ongoing
                    setTimeout(checkProcessingStatus, pollInterval);
                }
            } catch (error) {
                console.error('Error while polling:', error);
                setProcessing(false); // Reset processing state in case of error
            }
        };

        // Start polling
        checkProcessingStatus();
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
                                    <div className="image-placeholder-box">Background Preview</div>
                                )}
                    </div>
                    <div className='list-preview'>
                        <p>List Preview</p>
                        <input
                            type="file"
                            name="name-list"
                            accept=".csv, .xlsx, .xls"
                            onChange={handleNameListChange}
                        />
                        <div className="scrollable-container">
                            {nameListData.length > 0 ? (
                            <table>
                                <tbody>
                                {nameListData.map((row, rowIndex) => (
                                    <tr key={rowIndex}>
                                    {row.map((cell, cellIndex) => (
                                        <td key={cellIndex}>{cell}</td>
                                    ))}
                                    </tr>
                                ))}
                                </tbody>
                            </table>
                            ) : (
                            <div className="placeholder-box">Name-List Preview</div>
                            )}
                        </div>
                    </div>
                    <div className="auto-create-button">
                        <button type="submit" disabled={processing}>
                            {processing ? 'Processing...' : 'Generate'}
                        </button>
                    </div>
                </form>    
            </div>
        </div>
    )
}

export default Automatic;
