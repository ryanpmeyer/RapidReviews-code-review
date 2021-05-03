import {Card, List, Popup, Icon, Button, Header, Progress} from "semantic-ui-react";
import ReviewerFinderModal from "./RFModal";
import React from "react";

export default function ReviewerCard({reviewer, selected, avgScore}) {
    return (
        <Card className='blue card'>
            <Card.Content>
                <i class="right floated star icon" />
                <Card.Header target="_blank" href={`https://scholar.google.com/scholar?hl=en&q=+${encodeURIComponent(reviewer.name)}` }>{reviewer.name}</Card.Header>
                {reviewer.institution ?
                    <h4 class="ui sub header">{reviewer.institution}</h4> :
                    <h4 class="ui sub header">{}</h4>}
                <h4 className="ui sub header">{
                    <div>
                        Relevance Strength
                        {reviewer.score / avgScore * 50 > 75 ? <Progress percent={reviewer.score / avgScore * 40} color='green' /> :
                            <Progress percent={reviewer.score / avgScore * 50} color='yellow' />}
                    </div>
                }</h4>

                <Card color='red'/>
                {/*<Card.Meta>*/}
                {/*    <span className='date'>{reviewer.title}</span>*/}
                {/*</Card.Meta>*/}
                <Card.Description>

                    {/*{reviewer.abstract}*/}

                    <Header size='tiny'>Relevant Paper:</Header>
                    <List>
                    {reviewer.titles.map(function (item) {
                        return <List.Item target="_blank" href={`https://scholar.google.com/scholar?hl=en&q=+${encodeURIComponent(item)}` } icon='paperclip' content={item}/>;
                    })}
                    </List>
                </Card.Description>
                {/*<a className="ui tag label" href="#/">COVID-19</a>*/}
            </Card.Content>
            {/*<Card.Content extra>*/}
            {/*    <Tooltip title="Send an invitation to this reviewer">*/}
            {/*        <Mbutton*/}
            {/*            variant="outlined"*/}
            {/*            color="primary"*/}
            {/*            endIcon={<i className="envelope icon small"/>}*/}
            {/*        >Invite</Mbutton></Tooltip>*/}
            {/*    <Tooltip title="Click to see more information about this reviewer">*/}
            {/*        <ReviewerFinderModal/>*/}
            {/*    </Tooltip>*/}
            {/*</Card.Content>*/}
        </Card>
    );
}

