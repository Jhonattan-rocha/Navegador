import React from "react";
import { ToggleSwitch } from "../styles";

export default function Appearance(props){
    return (
        <div><ToggleSwitch><input type="checkbox" /><span className="slider"></span></ToggleSwitch></div>
    );
}
