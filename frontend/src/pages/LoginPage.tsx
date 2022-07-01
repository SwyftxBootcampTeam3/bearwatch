import { Container, FormGroup, TextField, Paper, Box, FormControlLabel, Checkbox, FormLabel, Button, Typography } from '@mui/material';
import React, { useState } from 'react';

export default function LoginPage() {
    const defaultValues = {
        email: "",
        ph: "",
        // alertType: "email",
        // password: ""
    };

    const [formValues, setFormValues] = useState(defaultValues);

    const handleSignUp = () => {
        console.log(formValues)
    }

    const handleLogin = () => {
        console.log(formValues)
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
    </>
    )
    
}