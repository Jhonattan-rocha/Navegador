import styled from "styled-components";
import {azulescuro } from '../../config/colors';

export const Title = styled.h1`
    color: ${props => {return props.isRad? "black": "black"}};
    text-align: center;
    small{
        font-size: 12pt;
        margin-left: 15px;
        color: #BDBDBD;
    }
`;


export const ContainerPrincipal = styled.div`
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    background: linear-gradient(to right, #050A30 60%,  #233DFF 40%);
`;

export const ContainerSection = styled.div`
    width: 100%;
    height: 60%;
    display: flex;
    justify-content: flex-end;
    flex-direction: row;
    align-items: center;
    padding-left: 50px;
    padding-right: 445px;
`;


export const ImgLogo = styled.img`
    width: 300px;
    height: 200px;
    margin-left: 40px;
    margin-bottom: 40px;
`;

export const InputForm = styled.div`
    margin-bottom: 10px;
    height: 50px;
    width: 344px;
    border: none;
    border-radius: 10px;
    font-size: 16px;
    background-color: #cacaca;
    padding: 0 10px;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    flex-direction: row;

    input {
        width: 80%;
        height: 100%;
        border: none;
        background-color: #cacaca;
        border-radius: 20px;
        margin-left: 10px;
    }
`;

export const Form = styled.form`
    background-color: white;
    max-width: 500px;
    width: 70%;
    padding: 20px;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    border-radius: 20px;

    h3{
    font-size: 30px;
    text-align: center;
    color: #050A30;
    font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }
    input[type=text],
    input[type=password]{
        width: 100%;
        height: 40px;
        border-radius: 10px;
        border: 1px solid #ccc;
        padding-left: 10px;
        margin-top: 10px;

        :focus{
            border: 1px solid ${azulescuro};
        }
    }
    input[type=submit]{
        width: 100%;
        height: 40px;
        cursor: pointer;
        background-color: #050A30;
        color: white;
        border:0;
        border-radius: 10px;
        margin-top: 10px;
    }
    input[type=submit]:hover{
    background-color: #233DFF;   
    }
`;

