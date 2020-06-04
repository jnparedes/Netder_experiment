import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import copy
import bisect
from datetime import datetime
from Ontological.Variable import Variable
from Ontological.Null import Null
from Ontological.OntDB import OntDB
from Diffusion_Process.NetDiffProgram import NetDiffProgram
from Diffusion_Process.NetDiffInterpretation import NetDiffInterpretation

class NetDERChase:

	def __init__(self, kb, tmax = 1):
		self._kb = kb
		self._tmax = tmax
		self._net_diff_interpretation = NetDiffInterpretation(self._kb.get_net_diff_graph(), self._tmax)
		self._body_mapping_his = []
		self._rule_map_his = {}

	def _get_atom_mapping(self, atom, data_base):
		result = []
		for data in data_base:
			if atom.is_mapped(data):
				mapping = atom.get_mapping(data)
				result.append(mapping)
				if mapping == {}:
					break
		if len(result) == 0:
			result = None
		
		return result

	def _get_atoms_mapping(self, atoms, data_base):
		aux_result = [[]]
		aux_mapped_atoms = [copy.deepcopy(atoms)]

		for index in range(0, len(atoms)):
			mapped_atoms = aux_mapped_atoms
			result = aux_result
			aux_mapped_atoms = []
			aux_result = []
			for ma_index in range(0, len(mapped_atoms)):
				mapping_atom_list = self._get_atom_mapping(mapped_atoms[ma_index][index], data_base)
				if (not mapping_atom_list is None):
					for mapping_atom in mapping_atom_list:
						other_mapping = copy.deepcopy(result[ma_index])
						other_mapping.append(mapping_atom)
						aux_result.append(other_mapping)
						cloned_mapped_atoms = copy.deepcopy(mapped_atoms[ma_index])
						for otherAtom in cloned_mapped_atoms:
							otherAtom.map(mapping_atom)
	
						aux_mapped_atoms.append(cloned_mapped_atoms)

		return aux_result

	def _get_candidate_atoms(self, rule):
		candidates = []
		atom_ids = []
		for atom in rule.get_ont_body():
			if not atom.getId() in atom_ids:
				candidates = candidates + self._kb.get_data_from_pred(atom.getId())
				atom_ids.append(atom.getId())
		
		for nct in rule.get_net_body():
			candidates = candidates + self._kb.get_data_from_pred(nct.getComponent().getId())

		return candidates

	def _search_body_mapping(self, atoms):
		ont_bd = OntDB(atoms)
		result = None
		for bm in self._body_mapping_his:
			if ont_bd.is_equivalent(bm[0]):
				result = bm[1]
				break

		return result

	def get_body_mapping(self, rule, time):
		net_db = []
		cloned_net_body = copy.deepcopy(rule.get_net_body())
		for nct in cloned_net_body:
			net_db.append(nct.getComponent())



		#body_mapping = self._get_atoms_mapping(rule.get_ont_body() + net_db, self._kb.get_ont_data() + self._kb.get_net_data())
		body_mapping = self._search_body_mapping(rule.get_ont_body() + net_db)

		if body_mapping is None:
			body_mapping = self._get_atoms_mapping(rule.get_ont_body() + net_db, self._get_candidate_atoms(rule))
			ont_db = OntDB(rule.get_ont_body() + net_db)
			self._body_mapping_his.append((ont_db, body_mapping))


		aux_body_mapping = []
		if len(body_mapping) > 0:

			for possibility in body_mapping:
				net_db = []
				cloned_net_body = copy.deepcopy(rule.get_net_body())
				for nct in cloned_net_body:
					net_db.append(nct.getComponent())
				for mapping in possibility:
					for atom in net_db:
						atom.map(mapping)
				
				if (len(time) > 0):

					if len(cloned_net_body) > 0:
						for nct in cloned_net_body:
							comp = self._kb.get_comp_from_atom(nct.getComponent())
							for t in range(time[0], time[1] + 1):
								if self._net_diff_interpretation.isSatisfied(t, comp, (nct.getLabel(), nct.getBound())):
									if self._net_diff_interpretation.areSatisfied(t, self._kb.get_net_diff_graph(), rule.get_global_cond()):
										aux_body_mapping.append(possibility)

					else:
					#elif len(rule.get_global_cond()) > 0:
						for t in range(time[0], time[1] + 1):
							if self._net_diff_interpretation.areSatisfied(t, self._kb.get_net_diff_graph(), rule.get_global_cond()):
								aux_body_mapping.append(possibility)
					
				else:
					aux_body_mapping = body_mapping

		body_mapping = aux_body_mapping

		return body_mapping


	def applyStepTGDChase(self, tgd, time):
		result = []
		applicable = True

		body_mapping = self.get_body_mapping(tgd, time)
		
		ont_head_result = []
		net_head_result = []

		if len(body_mapping) > 0:
			if not (tgd.get_id() in self._rule_map_his.keys()):
				self._rule_map_his[tgd.get_id()] = []

			mapping_his = self._rule_map_his[tgd.get_id()]
			
			#found_mapping = False
			
			
			cloned_body_mapping = copy.deepcopy(body_mapping)
			body_mapping_index = 0
			possibility_to_remove = []
			for possibility in cloned_body_mapping:
				key_mapping = ""
				for mapping in possibility:
					for key in mapping.keys():
						key_mapping = key_mapping + str(key) + str(mapping[key])

				value = hash(key_mapping)
				index = bisect.bisect_left(mapping_his, value)
			
				if index < len(mapping_his) and mapping_his[index] == value:
				#if key_mapping in mapping_his:
					possibility_to_remove.append(body_mapping[body_mapping_index])

				else:
					self._rule_map_his[tgd.get_id()].append(value)
					#self._rule_map_his[tgd.get_id()] = value
					self._rule_map_his[tgd.get_id()].sort()
					#self._rule_map_his[tgd.get_id()].append(key_mapping)

				body_mapping_index += 1
			
			for possibility in possibility_to_remove:
				body_mapping.remove(possibility)

			for possibility in body_mapping:
				net_head_comp = []
				cloned_net_head = copy.deepcopy(tgd.get_net_head())
				for nct in cloned_net_head:
					net_head_comp.append(nct.getComponent())
				cloned_ont_head = copy.deepcopy(tgd.get_ont_head())
				for mapping in possibility:
					for atom in cloned_ont_head:
						atom.map(mapping)
					for comp in net_head_comp:
						comp.map(mapping)
				ont_head_result.append(cloned_ont_head)
				net_head_result.append(cloned_net_head)
			
		aux_result = [[], []]
		index = 0
		for possibility in ont_head_result:
			for atom in possibility:
				for term in atom.get_terms():
					if isinstance(term, Variable):
						null = Null()
						for atom in possibility:
							atom.map({term.getId(): null})
						for nct in net_head_result[index]:
							nct.getComponent().map({term.getId(): null})
			aux_result[0] = aux_result[0] + possibility

		for possibility in net_head_result:
			for nct in possibility:
				for term in nct.getComponent().get_terms():
					if isinstance(term, Variable):
						null = Null()
						for nct in possibility:
							nct.getComponent().map({term.getId(): null})
			aux_result[1] = aux_result[1] + possibility



		return aux_result

	def applyStepEGDChase(self, egd, time):
		success = True

		body_mapping = self.get_body_mapping(egd, time)

		new_mapping = {}
		if len(body_mapping) > 0:
			for possibility in body_mapping:
				head = copy.deepcopy(egd.get_head())
				cloned_ont_body1 = copy.deepcopy(egd.get_ont_body())
				cloned_net_body1 = copy.deepcopy(egd.get_net_body())
				cloned_ont_body2 = copy.deepcopy(egd.get_ont_body())
				cloned_net_body2 = copy.deepcopy(egd.get_net_body())
				for atom in cloned_ont_body1:
					atom.map({head[0].getId(): head[1]})
					for mapping in possibility:
						atom.map(mapping)
				for nct in cloned_net_body1:
					nct.getComponent().map({head[0].getId(): head[1]})
					for mapping in possibility:
						nct.getComponent().map(mapping)

				head = copy.deepcopy(egd.get_head())
				for atom in cloned_ont_body2:
					atom.map({head[1].getId(): head[0]})
					for mapping in possibility:
						atom.map(mapping)
				for nct in cloned_net_body2:
					nct.getComponent().map({head[1].getId(): head[0]})
					for mapping in possibility:
						nct.getComponent().map(mapping)

				for index in range(0, len(cloned_ont_body1)):
					term_i = 0
					for term in cloned_ont_body1[index].get_terms():
						if term.can_be_instanced():
							new_mapping[term.getId()] = cloned_ont_body2[index].get_terms()[term_i]
						elif cloned_ont_body2[index].get_terms()[term_i].can_be_instanced():
							new_mapping[cloned_ont_body2[index].get_terms()[term_i].getId()] = term
						elif (not term.getValue() == cloned_ont_body2[index].get_terms()[term_i].getValue()):
							success = False
							break
							break

						term_i = term_i + 1
				for index in range(0, len(cloned_net_body1)):
					term_i = 0
					for term in cloned_net_body1[index].getComponent().get_terms():
						if term.can_be_instanced():
							new_mapping[term.getId()] = cloned_net_body2[index].getComponent().get_terms()[term_i]
						elif cloned_net_body2[index].getComponent().get_terms()[term_i].can_be_instanced():
							new_mapping[cloned_net_body2[index].getComponent().get_terms()[term_i].getId()] = term
						elif (not term.getValue() == cloned_net_body2[index].getComponent().get_terms()[term_i].getValue()):
							success = False
							break
							break
						term_i = term_i + 1
			if (success):
				self._kb.apply_map(new_mapping)

		return success

	def answer_query(self, query, int_bound):
		result = []
		seguir = True
		counter = 0
		self._net_diff_interpretation = NetDiffInterpretation(self._kb.get_net_diff_graph(), self._tmax)
		while(counter <= int_bound and seguir):
			mapping_list = []
			while(seguir):
				new_knowledge = [[], []]
				index = 0
				for tgd in self._kb.get_netder_tgds():
					inicio = datetime.now()
					TGD_result = self.applyStepTGDChase(tgd, query.get_time())
					fin = datetime.now()
					#print('Time TGD: ', index, fin - inicio)
					index += 1
					new_knowledge[0] = new_knowledge[0] + TGD_result[0]
					new_knowledge[1] = new_knowledge[1] + TGD_result[1]
				
				
				success = self._kb.add_ont_knowledge(new_knowledge[0])
				self._kb.add_net_knowledge(new_knowledge[1], query.get_time())

				for egd in self._kb.get_netder_egds():
					seguir = self.applyStepEGDChase(egd, query.get_time())
					print('seguir egd')
					print(seguir)
					if not seguir:
						break
				self._body_mapping_his = []
				if seguir:
					qa_success = True
					mapping_list = []				
					for q in query.get_disjoint_queries():
						candidates = self._get_candidate_atoms(q)
						q_mapping_list = self._get_atoms_mapping(q.get_ont_body(), candidates)
						
						mapping_list = mapping_list + q_mapping_list
						
						if not (len(q_mapping_list) > 0):
							qa_success = False
					#if (len(mapping_list) > 0) or (len(new_knowledge[0]) == 0 and len(new_knowledge[1]) == 0):
					if (qa_success) or ((not success) and len(new_knowledge[1]) == 0):
						seguir = False
				else:
					mapping_list = []

			if not qa_success and len(mapping_list) > 0:
				qa_success = True

			'''
			if qa_success:
				result = []
				for possibility in mapping_list:
					aux_result_mapping = {}
					for mapping in possibility:
						for key in mapping.keys():
							if not (Variable(key) in query.get_exist_var()):
								aux_result_mapping[key] = mapping[key]
					if len(aux_result_mapping) > 0:
						result.append(aux_result_mapping)

			else:
				net_diff_program = NetDiffProgram(self._kb.get_net_diff_graph(), self._tmax, self._kb.get_net_diff_facts(), self._kb.get_net_diff_lrules(), self._kb.get_net_diff_grules())
				self._net_diff_interpretation = net_diff_program.diffusion()
				result = None
				seguir = True'''
			net_diff_program = NetDiffProgram(self._kb.get_net_diff_graph(), self._tmax, self._kb.get_net_diff_facts(), self._kb.get_net_diff_lrules(), self._kb.get_net_diff_grules())
			self._net_diff_interpretation = net_diff_program.diffusion()
			result = None
			seguir = True
			counter = counter + 1
			print('final net_diff_interpretation')
			print(str(self._net_diff_interpretation))
		result = []
		for possibility in mapping_list:
			aux_result_mapping = {}
			for mapping in possibility:
				for key in mapping.keys():
					if not (Variable(key) in query.get_exist_var()):
						aux_result_mapping[key] = mapping[key]
			if len(aux_result_mapping) > 0:
				result.append(aux_result_mapping)

		return result

