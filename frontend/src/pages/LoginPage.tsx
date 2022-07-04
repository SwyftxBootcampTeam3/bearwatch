import { Container, FormGroup, TextField, Paper, Box, FormControlLabel, Checkbox, FormLabel, Button, Typography, Alert } from '@mui/material';
import { AxiosError, AxiosResponse } from 'axios';
import { isNil } from 'lodash';
import React, { FC, useState } from 'react';
import UserService from '../services/user.service';
import { User, Token } from '../types/models';
import { RegisterRequest } from '../types/requests';


interface LoginProps {
    handleAuth:(token: Token) => void;
  }


const LoginPage: FC<LoginProps> = (props: LoginProps) => {
    const defaultValues = {
        email: "",
        phone_number: ""
    };

    const [formValues, setFormValues] = useState(defaultValues);
    const [loginError, setLoginError] = useState<string | null>(null);
    const [signUp, setSignUp] = useState<boolean>(true);

    const handleSignUp = async () => {
        try {
            const registerRequest: RegisterRequest = {
                email: formValues.email,
                phone_number: formValues.phone_number
            }
            const res:AxiosResponse = await UserService.register(registerRequest);
            const token:Token = res.data;
            props.handleAuth(token);
        } catch (err:any){
            if (err.response.status === 400){
                setLoginError(err.response.data.detail)
            }else if (err.response.status === 422){
                setLoginError('Invalid Email!')
            }
            else{
                setLoginError('An unknown error has occured. Please try again later!')
            }
        }
    }

    const handleLogin = async () => {
        try {
            const res:AxiosResponse = await UserService.login(formValues.email);
            const token:Token = res.data;
            props.handleAuth(token);
        } catch (err:any){
            if (err.response.status === 401){
                setLoginError('No account exists with this email!')
            }else if (err.response.status === 422){
                setLoginError('Invalid Email!')
            }
            else{
                setLoginError('An unknown error has occured. Please try again later!')
            }
        }
    }

    return (
        <>
        <Box
        sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            height: '80vh',
        }}
        >
        <Paper variant="outlined" sx={{padding: 10}} square>
            {signUp && <Typography variant="h6">Sign Up</Typography>}
            {!signUp && <Typography variant="h6">Log In</Typography>}
            <br/>
            <FormGroup>
                <TextField id="outlined-basic" label="Email" variant="outlined" required onChange={(evt) => { setFormValues({...formValues, email: evt.target.value})}}/>
                <br/>
                {signUp && 
                <>
                    <TextField id="outlined-basic" label="Phone Number" variant="outlined" required onChange={(evt) => { setFormValues({...formValues, phone_number: evt.target.value})}}/>
                    <br/>
                </>
                }
                {signUp && 
                    <Button variant="contained" onClick={handleSignUp}>Sign Up</Button>
                }
                {!signUp && 
                <Button variant="contained" onClick={handleLogin}>Login</Button>
                }
            </FormGroup>
        <br/>
        {signUp && 
            <Button variant="text" onClick={() => setSignUp(!signUp)}>Log in here</Button>
        }
        {!signUp && 
            <Button variant="text" onClick={() => setSignUp(!signUp)}>Sign up here</Button>
        }
        </Paper>
        </Box>
        {loginError !== null && <Alert severity='error' onClose={() => {setLoginError(null)}}>{loginError}</Alert>}
    </>
    )
    
}
export default LoginPage;