// SmartCurriculum - Loading Spinner Component

import React from 'react';
import './LoadingSpinner.css';

function LoadingSpinner({ size = 'md', message = '' }) {
    const sizeClass = {
        sm: 'spinner-sm',
        md: '',
        lg: 'spinner-lg'
    }[size];

    return (
        <div className="loading-container">
            <div className={`spinner ${sizeClass}`}></div>
            {message && <p className="loading-message">{message}</p>}
        </div>
    );
}

export default LoadingSpinner;
