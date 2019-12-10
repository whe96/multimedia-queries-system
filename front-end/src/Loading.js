import React from "react";

import './Loading.css'

function Loading(props) {
    return (
        <div className="loading">
            <div className="sk-chase">
                <div className="sk-chase-dot"/>
                <div className="sk-chase-dot"/>
                <div className="sk-chase-dot"/>
                <div className="sk-chase-dot"/>
                <div className="sk-chase-dot"/>
                <div className="sk-chase-dot"/>
            </div>
        </div>
    );
}

export default Loading;
