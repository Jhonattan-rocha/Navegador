import axios from 'axios';
import { ApiPort, baseURL } from '../config/appConfig';

export default axios.create({
    baseURL: `http://${baseURL}:${ApiPort}/`,
    headers: {"Content-Type":"application/json"}
});
    