import React, {useState, Fragment} from 'react';
import Container from '@material-ui/core/Container';
import {Card, Form, Input, Loader} from 'semantic-ui-react'
import './reviewer-finder.css'
import 'semantic-ui-css/semantic.min.css';
import 'bootstrap';
import ReviewerFinderModal from './RFModal.js'
import ReviewerCard from "./ReviewerCard";
import {Get} from "../../../shared/Fetcher";
import {DecorateParams} from "../../Auth/login";
import {withRouter} from "react-router";
import { throttle } from "lodash";

const qs = require('qs');

function arrayAverage(reviewers){
    //Find the sum
    var sum = 0;
    for(var i in reviewers) {
        sum += reviewers[i].score;
    }
    //Get the length of the array
    var numbersCnt = reviewers.length;
    //Return the average / mean.
    return (sum / numbersCnt);
}

class ReviewerFinder extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            query: '',
            loading: false,
            reviewers: [],
            paper_id: qs.parse(this.props.location.search, {ignoreQueryPrefix: true}).paper_id,
        };
        this.handleFormSubmit = this.handleFormSubmit.bind(this);
        this.handleInputChange = this.handleInputChange.bind(this);
    }

    getpaper = (paper_id) => {
        const that = this;
        Get(`/entries/${paper_id}`, DecorateParams({}))
            .promise()
            .then(response => {
                that.setState(response);
            }).catch( (error) => {
                console.log(error);
                that.setState({title:null, abstract:null, authors:null, journal:null});
            }
        );
    };

    searchReviewers = (paper_id) => {
        const that = this;
        this.setState({
            loading: true
        });
        Get(`/reviews/S3/${paper_id}/find_reviewers?query=${this.state.query}`)
            .promise()
            .then(response => {
                const reviewers = response["recommended_reviewers"];
                that.setState(
                    {
                        reviewers,
                        loading: false
                    });
            }).catch((error) => {
                that.setState({loading:false, reviewers:[]})
        });
    };

    handleFormSubmit = () => {
        this.searchReviewers(this.state.paper_id, this.state.query)
    };

    handleInputChange = (e) => {
        this.setState({
            query: e.target.value,
        });
        if (this.state.query === "" || this.state.query === null) {
            this.searchReviewers(this.state.paper_id, this.state.query);
        }
    };

    componentDidMount() {
        this.getpaper(this.state.paper_id);
        this.searchReviewers(this.state.paper_id);
    }





    render() {
        return (
            <Fragment>
                <h1 >
                    {this.state.title ? this.state.title : ""}
                </h1>
                <h3 >
                    {this.state.authors ? this.state.authors.map((a) => {return a.name}).join(", ") : ""}
                </h3>
                <div>
                    {this.state.abstract ? this.state.abstract : ""}
                </div>
                <h4 className="ui horizontal divider header">
                    <i className="info circle icon"/>
                    AI-Suggested Reviewers
                </h4>
                <Fragment>
                    <div className="searchbox">
                        <Form onSubmit={this.handleFormSubmit}>
                            <Form.Input placeholder='Filter researchers by keyword...'
                                        value={this.state.query}
                                        onChange={this.handleInputChange}
                                        icon="search"/>
                        </Form>
                    </div>
                </Fragment>
                <div>

                    {this.state.loading ? <Loader active inline/> :
                        <Card.Group>
                            {this.state.reviewers.map(el => (
                                <ReviewerCard reviewer={el} avgScore={arrayAverage(this.state.reviewers)}/>
                            ))}
                        </Card.Group>}
                </div>
            </Fragment>
        );
    }
}

export default withRouter(ReviewerFinder);
