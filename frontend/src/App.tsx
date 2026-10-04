import AppBar from '@mui/material/AppBar';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import { Navigate, NavLink, Route, Routes } from 'react-router-dom';

import { APP_TITLE, NAV_LABELS } from './constants/messageConstants';
import { ROUTES } from './constants/routeConstants';
import EmployeesPage from './views/pages/EmployeesPage';
import InsightsPage from './views/pages/InsightsPage';

export default function App() {
  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            {APP_TITLE}
          </Typography>
          <Button color="inherit" component={NavLink} to={ROUTES.EMPLOYEES}>
            {NAV_LABELS.EMPLOYEES}
          </Button>
          <Button color="inherit" component={NavLink} to={ROUTES.INSIGHTS}>
            {NAV_LABELS.INSIGHTS}
          </Button>
        </Toolbar>
      </AppBar>
      <Container sx={{ py: 4 }}>
        <Routes>
          <Route path={ROUTES.ROOT} element={<Navigate to={ROUTES.EMPLOYEES} replace />} />
          <Route path={ROUTES.EMPLOYEES} element={<EmployeesPage />} />
          <Route path={ROUTES.INSIGHTS} element={<InsightsPage />} />
        </Routes>
      </Container>
    </>
  );
}
