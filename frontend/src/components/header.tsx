import React, { FC } from 'react';
import {AppBar, Container, Toolbar, Typography} from '@mui/material';

interface HeaderProps {
  title: string;
  subtitle: string;
  user: string;
}

const Header: FC<HeaderProps> = ({ title, subtitle, user }) => {
  return (
    <>
    <AppBar position="static">
        <Container>
          <Toolbar disableGutters>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                {title}
            </Typography>
          </Toolbar>
        </Container>
     </AppBar>
    </>
  );
};

export default Header;