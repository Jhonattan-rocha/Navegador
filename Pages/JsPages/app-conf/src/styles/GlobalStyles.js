import styled, { createGlobalStyle } from "styled-components";
import * as colors from "../config/colors";
import 'react-toastify/dist/ReactToastify.css'

export default createGlobalStyle`
    * {
        margin: 0;
        padding: 0;
        outline: none;
        box-sizing: border-box;
    }

    body{
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        background: ${colors.azulescuro};
        color: ${colors.azulescuro};
    }

    html, body, #root{
        height: 100%;
    }

    #root{
        display: flex;
        align-items: start;
        flex-direction: column;
        justify-content: start;
        flex-grow: 1;
        position: relative;
    }

    button{
        width: 200px;
        height: 40px;
        padding: 10px;
        cursor: pointer;
        background-color: #050A30;
        color: white;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        border:0;
        border-radius: 10px;
        margin-top: 10px;
    }

    a {
        text-decoration: none;
        color: ${colors.azulescuro};
    }

    ul {
        list-style: none;
    }

    p {
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif
    }

    h3{
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif
    }

    label{
        font-size: 16px;
    }

    body .Toastify .Toastify__toast-container .Toastify__toast--success{
        background-color: ${colors.azulescuro};
        color: white;
    }

    body .Toastify .Toastify__toast-container .Toastify__toast--error{
        background-color: ${colors.errorColor};
        color: white;
    }
    ::-webkit-scrollbar {
        width: 5px; /* Largura da barra de rolagem */
        margin-right: 5px; /* Margem à direita da barra de rolagem */
    }

    /* Estilizando o track da barra de rolagem */
    ::-webkit-scrollbar-track {
        background-color: #f1f1f1; /* Cor de fundo do track */
    }

    /* Estilizando o thumb (alça) da barra de rolagem */
    ::-webkit-scrollbar-thumb {
        background-color: #888; /* Cor do thumb */
    }

    /* Estilizando o thumb ao passar o mouse */
    ::-webkit-scrollbar-thumb:hover {
        background-color: #555; /* Cor do thumb ao passar o mouse */
    }
`;

export const Container = styled.section`
    width: 60%;
    min-height: 400px;
    background: #fff;
    margin: 30px auto;
    padding: 30px;
    border-radius: 4px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 1;
    flex-direction: column;
`;


export const DivCrescerBaixo = styled.div`
    width: 100%;
    position: relative;
    margin: auto;
    margin-top: 10px;
    margin-bottom: 10rem;
    display: flex;
    align-self: flex-end;
    flex-grow: 1;
`;
