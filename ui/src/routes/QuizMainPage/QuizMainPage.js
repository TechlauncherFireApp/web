import 'bootstrap/dist/css/bootstrap.min.css';
import './QuizMainPage.scss';

import React from 'react';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';

const QuizMainPage = () => {
    return (
        <div>
            <h1>Assessment Centre</h1>
            <h3>Choose your role</h3>
            <Container>
            <Row xs={1} lg={3} xxl={4}>
                <Col>
                    <Card>
                        <Card.Img variant='top' src='https://www.rbgsyd.nsw.gov.au/getmedia/ce90c9e5-0e81-4904-94c8-5410a143bce7/placeholder_cross_1200x815.png'/>
                        <Card.Body>
                            <Card.Title>Role</Card.Title>
                            <Card.Text>Role description...</Card.Text>
                            <Button variant="danger">Proceed</Button>
                        </Card.Body>
                    </Card>
                </Col>

            </Row>
            </Container>
        </div>
    );
};

export default QuizMainPage;