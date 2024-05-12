import styled from "styled-components";

export const Container = styled.div`
  display: flex;
  height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
  width: 100%;
  height: 100%;
`;

export const Sidebar = styled.div`
  min-width: 200px;
  background: #f4f4f4;
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0,0,0,0.1);
`;

export const Content = styled.div`
  width: 100%;
  height: 100%;
  padding: 20px;
  background: #fff;
`;

export const Section = styled.div`
  padding: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  &:hover {
    background-color: #ddd;
  }
  border-radius: 10px;
  .active{
    background-color: #ddd;
  }
`;

export const Title = styled.h2`
  margin-bottom: 20px;
`;

export const Input = styled.input`
  width: 100%;
  padding: 8px 10px;
  margin-bottom: 10px;
  border: none;
  border-radius: 4px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
`;

export const ToggleSwitch = styled.label`
  position: relative;
  display: inline-block;
  width: 34px;
  height: 20px;

  & input {
    opacity: 0;
    width: 0;
    height: 0;
  }

  & .slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    transition: .4s;
    border-radius: 34px;
  }

  & .slider:before {
    position: absolute;
    content: "";
    height: 14px;
    width: 14px;
    left: 3px;
    bottom: 3px;
    background-color: white;
    transition: .4s;
    border-radius: 50%;
  }

  & input:checked + .slider {
    background-color: #2196F3;
  }

  & input:focus + .slider {
    box-shadow: 0 0 1px #2196F3;
  }

  & input:checked + .slider:before {
    transform: translateX(14px);
  }
`;

export const ContainerLabelToggle = styled.label`
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  flex-direction: row;
  margin-bottom: 10px;

  label{
    font-size: 20px;
  }
`;

export const ContainerCookies = styled.div`
    padding: 10px;
    border-radius: 10px;
    box-shadow: 1px 1px 1px 1px rgba(0,0,0,0.4);
    max-width: 50%;
    min-width: 500px;
    margin: auto;
`;