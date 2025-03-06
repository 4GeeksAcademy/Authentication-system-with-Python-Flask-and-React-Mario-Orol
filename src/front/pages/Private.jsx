import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import profileImage from "../assets/img/rigo-baby.jpg";

const Private = () => {
    const navigate = useNavigate();

    useEffect(() => {
        const token = sessionStorage.getItem("token");
        if (!token) {
            alert("You must be logged in to access this page.")
            navigate("/login")
        }
    }, []);

    return (
        <div className="container mt-5 text-center">
            <h2>Welcome to the Private Page!</h2>
            <p>This content is protected and only visible to logged-in users.</p>
            <img src={profileImage} alt="Profile" />
        </div>
    );
};

export default Private;
