import './QuizResult.scss';

import React, { useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import { useHistory } from 'react-router-dom';

const QuizResult = () => {
    const [correct, setCorrect] = useState(null);
    const [number, setNumber] = useState(null);
    const [role, setRole] = useState('');
    const history = useHistory();

    useEffect(() => {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const correctAmount = urlParams.get('correct').toLowerCase();
        const questionNumber = urlParams.get('number').toLowerCase();
        const roleType = urlParams.get('role').toLowerCase();
        setCorrect(correctAmount);
        setNumber(questionNumber);
        setRole(roleType);
    }, []);

    const handleRetakeQuiz = () => {
        history.push(`/questions/?roleType=${role}`);
    }

    const handleReturnMain = () => {
        history.push(`/quiz`);
    }

    return (
        <div className='quiz-result-container'>
            <Container>
                <div>
                    <Row><h1 className='quiz-result-heading'>RESULT</h1></Row>
                    <Row><hr className='quiz-hr'/></Row>
                    <Row sm={2}>
                        <Col><h4 className='quiz-result-txt'>{`You got ${correct} out of ${number} questions correct.`}</h4></Col>
                        <Col className='vertical-line'>
                            <Button className='quiz-result-btn' variant='danger' onClick={() => handleRetakeQuiz()}>Retake quiz</Button>
                            <Button className='quiz-result-btn' variant='danger' onClick={() => handleReturnMain()}>Return to main quiz page</Button>
                        </Col>
                    </Row>
                </div>
            </Container>
        </div>
    );
};

export default QuizResult;