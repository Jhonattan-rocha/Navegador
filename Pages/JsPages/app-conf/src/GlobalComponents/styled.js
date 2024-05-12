import styled, {keyframes} from "styled-components";

export const DivPopUp = styled.div`
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #fff;
    border: 1px solid #ccc;
    padding: 20px;
    z-index: 9;
    border-radius: 10px;
`;

export const DivOverLay = styled.div`
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 8;
`;


export const UploadContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: center;
  text-align: center;
  margin: 20px;
  align-self: center;
`;

export const Dropzone = styled.div`
  border: 2px dashed #ccc;
  padding: 20px;
  cursor: pointer;
  border-radius: 30px;
`;

export const ImgPreview = styled.div`
    border: 1px dashed black;
    border-radius: 50%;
    height: ${props => props.size ? `${props.size.container}px` :'150px'};
    width: ${props => props.size ? `${props.size.container}px` :'150px'};
    overflow: hidden;
    cursor: pointer;

    img{
        height: ${props => props.size ? `${props.size.img}px`:'200px'};
        width: ${props => props.size ? `${props.size.img}px`:'200px'};
        border-radius: 50%;
        position: relative;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        
    }
`;



export const Sidebar = styled.div`
  width: 0;
  height: 100%;
  position: fixed;
  display: flex;
  flex-direction: column;
  top: 0;
  right: 0;
  background-color: #fff;
  overflow-x: hidden;
  transition: 0.5s;
  border-left: 1px solid #333;
  z-index: 4;
  animation: ${({ open }) => (open ? slideIn : slideOut)} 0.5s forwards;
`;

export const slideIn = keyframes`
  from {
    width: 0;
  }
  to {
    width: 400px;
  }
`;

export const slideOut = keyframes`
  from {
    width: 400px;
  }
  to {
    width: 0;
  }
`;

export const SubHeaderContainer = styled.div`
    width: 100%;
    height: 140px;
    background-color: white;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-direction: row;
    padding: 0 70px;
`;
