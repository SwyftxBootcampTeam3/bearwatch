import { Container, FormGroup, TextField, Paper, Box, FormControlLabel, Checkbox, FormLabel, Button, Typography } from '@mui/material';
import React, { useState } from 'react';


interface LoginProps {
    toggleLogin: any
  }
  
export default function LoginPage(props: LoginProps) {
    const defaultValues = {
        email: "",
        ph: "",
        alertType: "email",
        password: ""
    };

    const [formValues, setFormValues] = useState(defaultValues);

    return (
        <>
        <Box
        sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            height: '100vh',
        }}
        >
        <Paper variant="outlined" sx={{padding: 10}} square>
            <Typography variant="h6">Create Account</Typography>
            <br/>
            <FormGroup>
                <TextField id="outlined-basic" label="Email" variant="outlined" required/>
                <br/>
                <TextField id="outlined-basic" label="Password" variant="outlined" type="password" required/>
                <br/>
                <TextField id="outlined-basic" label="Phone Number" variant="outlined" />
                <br/>
                <FormLabel sx={{display: 'flex',
                flexDirection: 'row'}} >Notification Type</FormLabel>
                <FormGroup aria-label='Notification Type' sx={{display: 'flex',
                flexDirection: 'row'}}>
                    <FormControlLabel control={<Checkbox defaultChecked />} label="Email" />
                    <FormControlLabel control={<Checkbox />} label="SMS" />
                </FormGroup>
                <Button variant="contained" onClick={() => {props.toggleLogin()}}>Submit</Button>
            </FormGroup>
            <p>Have an account? Sign in here</p>
        </Paper>
        </Box>
    </>
    )
    
}