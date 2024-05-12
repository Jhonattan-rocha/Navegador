import React from "react";
import { ToggleSwitch, ContainerLabelToggle, Input, ContainerCookies } from "../styles";

export default function Cookies(props){
    return (
        <ContainerCookies>
            <ContainerLabelToggle>
                <label>Save Cookies?</label>
                <ToggleSwitch>
                    <input type="checkbox" /><span className="slider"></span>
                </ToggleSwitch>
            </ContainerLabelToggle>
            <ContainerLabelToggle>
                <label>Path to save</label>
                <div><Input type="text" placeholder="Enter save path" /></div>
            </ContainerLabelToggle>
        </ContainerCookies>
    );
}
