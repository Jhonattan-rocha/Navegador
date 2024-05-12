import React, { useState, useEffect } from 'react';
import './styles.css';
import { ContainerPrincipal, ContainerSection, InputForm } from './styles';
import { FaUser } from 'react-icons/fa';
import { MdPassword } from 'react-icons/md';
import { AiOutlineEyeInvisible, AiOutlineEye } from 'react-icons/ai';
import { useDispatch, useSelector } from 'react-redux';
import * as actions from '../../store/modules/authReducer/actions';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';

function Login() {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [type, setType] = useState('password');
    const user = useSelector(state => state.authreducer);

    const dispatch = useDispatch();

  const handleLogin = () => {
    if(username.trim() === "" && password.trim() === ""){
        toast.error("Email ou senha não podem ser vazios")
        return;
    }
    dispatch(actions.Login({"email": username, "password": password}))
  };

  useEffect(() => {
    if(user.isLoggedIn){
        navigate("/");
    }
  }, [navigate, user]);

  return (
    <ContainerPrincipal>
        <ContainerSection>
            <div style={{ backgroundColor: 'darkpurple' }} className='login-page'>
                <span>Login</span>
                <InputForm>
                    <FaUser color='white' size={30}></FaUser>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Usuario"
                    />
                </InputForm>
                <InputForm>
                    <MdPassword color='white' size={30}></MdPassword>
                    <input
                        type={type}
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Senha"
                    />
                    {type === 'password' ? 
                    <AiOutlineEye size={30} color='white' onClick={() => setType('text')} cursor={'pointer'}></AiOutlineEye>
                    : 
                    <AiOutlineEyeInvisible size={30} color='white' onClick={() => setType('password')} cursor={'pointer'}></AiOutlineEyeInvisible>
                    }
                </InputForm>
                <p>Esqueci minha senha</p>
                <button onClick={handleLogin} style={{ color: 'white' }}>
                    Login
                </button>
            </div>
        </ContainerSection>
    </ContainerPrincipal>
  );
}

export default Login;
