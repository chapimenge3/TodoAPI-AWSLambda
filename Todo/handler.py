import os
import boto3
import json

TODO_TABLE = os.getenv('TODO_TABLE')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TODO_TABLE)

def create_todo(event, context):
    '''
    Create Todo Application in Dynamo DB
    
    Params:
        event: API Gateway Event
        context: Lambda Context
    
    Return:
        response: API Gateway Response
    
    response.body: JSON String
        message: String
        error: Boolean|String
    '''
    try:
        body = event['body']
        
        # check if the body is empty
        if body is None:
            raise Exception('Body is empty')

        # check if the body is a string and convert it to a dict
        if isinstance(body, str):
            body = json.loads(body)

        todo = body['todo']
        
        # check if the todo is empty
        if todo is None:
            raise Exception('Todo is empty')
        
        # check if todo is already in the table
        if table.get_item(Key={'todo': todo}).get('Item') is not None:
            raise Exception('Todo already exists')

        # create todo
        table.put_item(Item={'todo': todo, 'done': False})
        
        # return todoId
        response = {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Todo created',
                'error': False
            })
        }
        
        return response
        
    except Exception as e:
        # return error
        response = {
            'statusCode': 400,
            'body': json.dumps({
                'message': str(e),
                'error': True
            })
        }
        
        return response


def list_todo(event, context):
    '''
    List Todo Application in Dynamo DB
    
    Params:
        event: API Gateway Event
        context: Lambda Context
    
    Return:
        response: API Gateway Response
    
    response.body: JSON String
        message: String
        todos: List | None
        error: Boolean|String
    '''
    try:
        # list all todo
        response = table.scan()
        todos = response['Items']
        
        # return todos
        response = {
            'statusCode': 200,
            'body': json.dumps({
                'todos': todos,
                'error': False
            })
        }
        
        return response
        
    except Exception as e:
        # return error
        response = {
            'statusCode': 400,
            'body': json.dumps({
                'message': str(e),
                'error': True
            })
        }
        
        return response

def update_todo(event, context):
    '''
    Update Todo Application in Dynamo DB
    
    Params:
        event: API Gateway Event
        context: Lambda Context
    
    Return:
        response: API Gateway Response
    
    response.body: JSON String
        message: String
        error: Boolean|String
    '''
    try:
        body = event['body']
        
        # check if the body is empty
        if body is None:
            raise Exception('Body is empty')

        # check if the body is a string and convert it to a dict
        if isinstance(body, str):
            body = json.loads(body)

        todo = body['todo']
        
        # check if the todo is empty
        if todo is None:
            raise Exception('Todo is empty')
        
        # check if todo is already in the table
        if table.get_item(Key={'todo': todo}).get('Item') is None:
            raise Exception('Todo does not exist')

        # update todo
        table.update_item(
            Key={'todo': todo},
            UpdateExpression='SET done = :done',
            ExpressionAttributeValues={
                ':done': True
            }
        )
        
        # return todoId
        response = {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Todo updated',
                'error': False
            })
        }
        
        return response
        
    except Exception as e:
        # return error
        response = {
            'statusCode': 400,
            'body': json.dumps({
                'message': str(e),
                'error': True
            })
        }
        
        return response

def delete_todo(event, context):
    '''
    Delete Todo Application in Dynamo DB
    
    Params:
        event: API Gateway Event
        context: Lambda Context
    
    Return:
        response: API Gateway Response
    
    response.body: JSON String
        message: String
        error: Boolean|String
    '''
    try:
        body = event['body']
        
        # check if the body is empty
        if body is None:
            raise Exception('Body is empty')

        # check if the body is a string and convert it to a dict
        if isinstance(body, str):
            body = json.loads(body)

        todo = body['todo']
        
        # check if the todo is empty
        if todo is None:
            raise Exception('Todo is empty')
        
        # check if todo is already in the table
        if table.get_item(Key={'todo': todo}).get('Item') is None:
            raise Exception('Todo does not exist')

        # delete todo
        table.delete_item(Key={'todo': todo})
        
        # return todoId
        response = {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Todo deleted',
                'error': False
            })
        }
        
        return response
        
    except Exception as e:
        # return error
        response = {
            'statusCode': 400,
            'body': json.dumps({
                'message': str(e),
                'error': True
            })
        }
        
        return response