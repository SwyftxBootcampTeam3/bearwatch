import { Container, FormGroup, TextField, Paper, Box, FormControlLabel, Checkbox, FormLabel, Button, Typography, Alert } from '@mui/material';
import { AxiosError, AxiosResponse } from 'axios';
import { isNil } from 'lodash';
import React, { FC, useState } from 'react';
import UserService from '../services/user.service';
import { User, Token } from '../types/models';


interface LoginProps {
    handleAuth:(token: Token) => void;
  }


  const LoginPage: FC<LoginProps> = (props: LoginProps) => {
    const defaultValues = {
        email: "",
        ph: "",
        // alertType: "email",
        // password: ""
    };

    const [formValues, setFormValues] = useState(defaultValues);
    const [loginError, setLoginError] = useState<string | null>(null);

    const handleSignUp = () => {
        console.log(formValues)
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
            <Typography variant="h6">Account</Typography>
            <br/>
            <FormGroup>
                <TextField id="outlined-basic" label="Email" variant="outlined" required onChange={(evt) => { setFormValues({...formValues, email: evt.target.value})}}/>
                <br/>
                {/* <TextField id="outlined-basic" label="Password" variant="outlined" type="password" required onChange={(evt) => { setFormValues({...formValues, password: evt.target.value})}}/>
                <br/> */}
                <TextField id="outlined-basic" label="Phone Number" variant="outlined" required onChange={(evt) => { setFormValues({...formValues, ph: evt.target.value})}}/>
                <br/>
                {/* <FormLabel sx={{display: 'flex',
                flexDirection: 'row'}} >Notification Type</FormLabel> */}
                {/* <FormGroup aria-label='Notification Type' sx={{display: 'flex',
                flexDirection: 'row'}}>
                    <FormControlLabel control={<Checkbox defaultChecked />} label="Email" />
                    <FormControlLabel control={<Checkbox />} label="SMS" />
                </FormGroup> */}
                <div>
                    <Button variant="contained" onClick={handleSignUp}>Sign Up</Button>
                    &nbsp;
                    <Button variant="contained" onClick={handleLogin}>Login</Button>
                </div>
            </FormGroup>
        </Paper>
        </Box>
        {loginError !== null && <Alert severity='error' onClose={() => {setLoginError(null)}}>{loginError}</Alert>}
    </>
    )
    
}
export default LoginPage;