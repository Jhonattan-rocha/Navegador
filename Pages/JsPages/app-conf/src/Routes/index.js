import React from "react";
import { Route, Routes } from "react-router-dom";

import Login from "../pages/Login";
import NoPage from "../pages/NoPage";
import Config from "../pages/Config";

export default function Rotas(){


    return (
        <>
            <Routes>
                <Route path="/config" element={
                    <Config></Config>
                }/>
                <Route path="/login" index element={<Login></Login>}/>
                <Route path="*" element={<NoPage/>}/>
            </Routes>
        </>
    );
};
