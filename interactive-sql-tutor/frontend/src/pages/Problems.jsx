import { Navbar, Container, ProblemList } from '../components';

export default function Problems() {
  return (
    <>
      <Navbar selected={1} />
      <Container>
        <ProblemList />
      </Container>
    </>
  );
}
