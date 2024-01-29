// import {CameraAccess} from "./cameraAccess";
import { useNavigate } from "react-router-dom";


export const BackButton = ({className, route=-1}) => {

    const navigate = useNavigate()

    const handleNavigate = (path) => {
        navigate(path)
    }

    return (
        <button className={className} onClick={() => handleNavigate(route)}>Back</button>
    )
}
