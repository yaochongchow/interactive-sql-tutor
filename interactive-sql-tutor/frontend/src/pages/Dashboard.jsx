import { Login } from '.';
import {
  Navbar,
  Container,
  StudentDashboard,
  InstructorDashboard,
} from '../components';
import { useAuth } from '../utils/hooks';

export default function Dashboard() {
  const { authInfo } = useAuth();
  const { profile, isLoggedIn } = authInfo;
  if (!isLoggedIn) return <Login />;
  
  return (
    <>
      <Navbar selected={0} />
      <Container>
        {profile.role === 'Student' ? (
          <StudentDashboard />
        ) : (
          <InstructorDashboard />
        )}
      </Container>
    </>
  );
}
