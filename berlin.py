#!/usr/bin/env python

import json
import logging
import random
import heapq
import time

import ai

version = "0.1"

class Node:

  def __init__(self, id, points, units_per_turn, owner=None, units=0):
    self.id=id
    self.points=points
    self.units_per_turn=units_per_turn
    self.owner=owner
    self.units=units
    self.edges=[] # outgoing edges (id)

  def __repr__(self):
    return 'Node: id:%s, points:%s, units_per_turn:%s owner:%s, units:%s, edges:%s' % \
      (self.id, self.points, self.units_per_turn, self.owner, self.units, self.edges)

class Map:
  def __init__(self, mapdict, directed = False):
    try:
      self.directed = directed
      self.types = {}
      for t in mapdict['types']:
        self.types[t['name']] = {}
        self.types[t['name']]['points'] = t['points']
        self.types[t['name']]['units_per_turn'] = t['soldiers_per_turn']

      self.nodes = {} # should probably be a list, but largest map has
                      # less than 30 nodes, so whatever
      for n in mapdict['nodes']:
        self.nodes[n['id']] = Node(n['id'],
            self.types[n['type']]['points'],
            self.types[n['type']]['units_per_turn'])

      for p in mapdict['paths']:
        self.nodes[p['from']].edges.append(p['to'])
        if not self.directed:
          self.nodes[p['to']].edges.append(p['from'])
    except:
      logging.exception('failed to parse map')
      raise

  def __repr__(self):
    return 'Map: directed:%s, types:%s, nodes:%s' % \
        (self.directed, self.types, self.nodes)

  def update(self, statelist):
    for s in statelist:
      self.nodes[s['node_id']].owner = s['player_id']
      self.nodes[s['node_id']].units = s['number_of_soldiers']

class Game:
  def __init__(self, parsed_request):
    try:
      self.action = parsed_request['action']
      self.game_id = parsed_request['infos']['game_id']
      # assuming this is inclusive
      self.maxturns = parsed_request['infos']['maximum_number_of_turns']
      self.turn = parsed_request['infos']['current_turn']
      self.players = parsed_request['infos']['number_of_players']
      self.myself = parsed_request['infos']['player_id']
      self.timeout = parsed_request['infos']['time_limit_per_turn']
      self.directed = parsed_request['infos']['directed']
      self.m = Map(parsed_request['map'], self.directed)
      self.m.update(parsed_request['state'])
    except:
      logging.exception('failed to parse game')
      raise
  
  def __repr__(self):
    return 'Game: %s, %s, %s, %s, %s, %s, %s, %s' \
        % (self.action, self.game_id, self.maxturns, self.turn, self.players,
            self.myself, self.timeout, self.m)

  def generate_turn(self):
    '''
    do something here
    '''
    return ai.move_at_random(self)

class Response:
  def __init__(self):
    self.moves = []

  def add_move(self, origin, destination, units):
    self.moves.append({
      'from': origin,
      'to': destination,
      'number_of_soldiers': units })

  def __repr__(self):
    return json.dumps(self.moves)

def parse_request(request):
  logging.debug('received request: ' + str(request))
  try:
    game = Game(request)
    logging.debug('parsed request: ' + str(game))
  except:
    logging.exception('failed to parse request')
    return None
  return game