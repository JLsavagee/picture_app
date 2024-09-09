// Sidebar.js
import React from 'react';
import { Link } from 'react-router-dom';

const Sidebar = () => {
    return (
        <div style={{ width: '200px', background: '#f0f0f0', height: '100vh', padding: '20px' }}>
            <h2>Menu</h2>
            <ul style={{ listStyleType: 'none', padding: 0 }}>
                <li>
                    <Link to="/page1">
                        <button style={{ width: '100%' }}>Page 1</button>
                    </Link>
                </li>
                <li style={{ marginTop: '10px' }}>
                    <Link to="/page2">
                        <button style={{ width: '100%' }}>Page 2</button>
                    </Link>
                </li>
            </ul>
        </div>
    );
}

export default Sidebar;