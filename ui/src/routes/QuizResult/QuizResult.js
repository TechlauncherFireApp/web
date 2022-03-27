import './QuizResult.scss';

import React, { useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';

const QuizResult = () => {
    const [correct, setCorrect] = useState(null);
    const [number, setNumber] = useState(null);
    const [role, setRole] = useState('');

    useEffect(() => {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const correctAmount = urlParams.get('correct').toLowerCase();
        const questionNumber = urlParams.get('number').toLowerCase();
        const roleType = urlParams.get('role').toLowerCase();
        setCorrect(correctAmount);
        setNumber(questionNumber);
        setRole(roleType);
        console.log(role);
    }, []);

    return (
        <div>
            <Container>
                <div>
                    <Row><h1>RESULT</h1></Row>
                    <Row sm={2}>
                        <Col>{`You got ${correct} out of ${number} questions correct.`}</Col>
                        <Col>
                            <Button variant='danger'>Retake quiz</Button>
                            <Button variant='danger'>Return to main quiz page</Button>
                        </Col>
                    </Row>
                </div>
            </Container>
        </div>
    );
};

export default QuizResult;