// import {CameraAccess} from "./cameraAccess";
import { useLocation, useNavigate } from "react-router-dom";


export const SubmissionPage = () => {

    const location = useLocation();
    const test = location.state.test;

    const navigate = useNavigate()

    const handleNavigate = (path) => {
        navigate(path)
    }

    // return <CameraAccess></CameraAccess>
    return (
        <div>
            <div>
                <h1>This is the submission page!</h1>
                <a>{JSON.stringify(test)}</a>
            </div>
            <div>
                <button onClick={() => handleNavigate(-1)}>back</button>
            </div>
        </div>
    )
}
