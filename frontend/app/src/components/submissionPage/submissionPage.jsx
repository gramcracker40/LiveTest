// import {CameraAccess} from "./cameraAccess";
import { useLocation, useNavigate } from "react-router-dom";
import React, { useEffect, useContext, useState } from 'react';
import { EasyRequest, instanceURL, defHeaders } from '../../api/helpers';
import { AuthContext } from "../../context/auth";
import { TakeScantronPicture } from "../TakeScantronPicture";

export const SubmissionPage = () => {

    const { authDetails, updateAuthDetails } = useContext(AuthContext);
    const [capturedImage, setCapturedImage] = useState(null);
    const [errorOccurred, setErrorOccurred] = useState(false)
    const location = useLocation();
    const test = location.state.test;

    const navigate = useNavigate()


    const handleNavigate = (path) => {
        navigate(path)
    }

    useEffect(() => {
        // ------------------------ AUTHENTICATION DETAILS ---------------------------

        // if a user isn't logged in, take them back to the login page
        if (!authDetails.isLoggedIn) {
            navigate("/")
            return
        }
    }, [navigate, authDetails])

    const handleImageSubmit = (base64Image) => {
        console.log("base64Image: ", base64Image)
        setCapturedImage(base64Image);
        submitTest(base64Image);
    };

    const submitTest = async (image) => {

        console.log("image: ", image)

        // ------------------------- SUBMITTING STUDENT SCANTRON -------------------------
        const body = {
            "submission_photo": image,
            "file_extension": "png",
            "student_id": authDetails.id,
            "test_id": test.id
        }

        console.log("Body: ", body)

        const URL = instanceURL + "/submission/"

        try {
            let req = await (EasyRequest(URL, defHeaders, "POST", body))

            if (req.status === 200) {
                setErrorOccurred(false)
                navigate("/course")
                return
            }
            else {
                console.error("Error submitting scantron: ", req.status)
                setCapturedImage(null)
                setErrorOccurred(true)
                console.log("Setting error occured to true")
            }
        }
        catch (error) {
            console.error("API error", error)
        }
    }
    return (
        <div>
            <div>
                <h1>This is the submission page!</h1>
                {/* <a>{JSON.stringify(test)}</a> */}
            </div>
            <div>
                <button onClick={() => handleNavigate(-1)}>back</button>
            </div>
            {errorOccurred &&
                <div>
                    <span className="text-black">An Error occured, please try again</span>
                </div>
            }
            <TakeScantronPicture onSubmit={handleImageSubmit} />


        </div>
    )
}


