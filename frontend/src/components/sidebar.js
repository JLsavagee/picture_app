// Sidebar.js
import React from 'react';
import "./css/Sidebar.css";

const Sidebar = () => {
    return (
        <div className="sidebar">
            <h2>Menu</h2>
            <ul>
                <li>
                    <a href="/">
                        <button>Manual</button>
                    </a>
                </li>
                <li>
                    <a href="/page2">
                        <button>Automatic</button>
                    </a>
                </li>
            </ul>
        </div>
    );
}

export default Sidebar;