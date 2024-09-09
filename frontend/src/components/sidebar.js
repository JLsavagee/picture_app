// Sidebar.js
import React from 'react';
import { Link } from 'react-router-dom';
import "./css/Sidebar.css";

const Sidebar = () => {
    return (
        <div className="sidebar">
            <h2>Menu</h2>
            <ul>
                <li>
                    <a href="/page1">
                        <button>Page 1</button>
                    </a>
                </li>
                <li>
                    <a href="/page2">
                        <button>Page 2</button>
                    </a>
                </li>
            </ul>
        </div>
    );
}

export default Sidebar;