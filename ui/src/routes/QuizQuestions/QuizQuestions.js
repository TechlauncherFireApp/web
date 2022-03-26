import './QuizQuestions.scss';

import axios from 'axios';
import React, { useEffect, useState } from 'react';

import { backendPath } from '../../config';

const QuizQuestions = () => {
    const [questions, setQuestions] = useState([]);

    useEffect(() => {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const roleType = urlParams.get('roleType').toLowerCase().replace(/%20/g, " ");
        console.log('This is role type:' + roleType);

        const config = {
            'headers': {
                'withCredentials': true,
                'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
                'Content-Type': 'application/x-www-form-urlencoded',
                'Access-Control-Allow-Origin': '*'
            }
        };

        axios.get(backendPath + `quiz/getRandomQuestion?num=10&role=${roleType}&difficulty=1`, config)
            .then((res) => {
                setQuestions([...res.data]);
            })
            .catch((err) => {
                console.log(err);
            })
    });

    return (
        <div>
            <p>{questions}</p>
        </div>
    );
}

export default QuizQuestions;