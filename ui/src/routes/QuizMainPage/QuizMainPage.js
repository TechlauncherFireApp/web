import 'bootstrap/dist/css/bootstrap.min.css';
import './QuizMainPage.scss';

import axios from 'axios';
import React, { useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import { useHistory } from 'react-router-dom';

import { backendPath } from '../../config';

const QuizMainPage = () => {
    const [roles, setRoles] = useState([]);
    const history = useHistory();

    useEffect(() => {
        axios.get(backendPath + 'reference/roles')
            .then((res) => {
                setRoles([...res.data]);
            })
            .catch((err) => {
                console.log(err);
            })
    }, []);

    const handleClick = (role) => {
        history.push(`/questions/?roleType=${role}`);
    }

    return (
        <div>
            <h1>Assessment Centre</h1>
            <h3>Choose your role</h3>
            <Container>
            <Row xs={1} sm={2} lg={3} xxl={4}>
                {
                    roles.map((elem) => {
                        return (
                            <Col key={elem.id}>
                                <Card>
                                    <Card.Img variant='top' src='https://www.rbgsyd.nsw.gov.au/getmedia/ce90c9e5-0e81-4904-94c8-5410a143bce7/placeholder_cross_1200x815.png'/>
                                    <Card.Body>
                                        <Card.Title>{elem.name}</Card.Title>
                                        <Card.Text>Role description...</Card.Text>
                                        <Button variant="danger" onClick={() => handleClick(elem.name)}>Proceed</Button>
                                    </Card.Body>
                                </Card>
                            </Col>
                        )
                    })
                }
            </Row>
            </Container>
        </div>
    );
};

export default QuizMainPage;