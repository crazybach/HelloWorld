using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class UI3DModelView : MonoBehaviour {
	//public
	public List<GameObject> pivots = new List<GameObject>(); 
		
	//private
	private List<GameObject> models = new List<GameObject>();
	
	// Use this for initialization
	void Start () {
		/*
		model = GameObject.CreatePrimitive(PrimitiveType.Cube);
		model.transform.position = new Vector3(5.55f, 5.89f, 449.29f);
		model.transform.Rotate(45f,45f,45f);
		model.transform.localScale =new Vector3(100f,100f,100f);
		
		model.transform.parent = this.gameObject.transform;
		*/
		foreach(GameObject pivot in pivots){
			Object  protype = Resources.Load("mon_goblinWizard");
			if(protype == null){
				Debug.Log("Load Resources Error");
			}else{
				GameObject  model = (Instantiate(protype, pivot.transform.position, Quaternion.identity) as GameObject); 
				//GameObject.CreatePrimitive(PrimitiveType.Cube);
			
				//model.transform.position = pivot.transform.position;
				//model.transform.rotation = pivot.transform.rotation;
				//model.transform.localScale = new Vector3(0.5f, 0.5f, 0.5f);
		
				models.Add(model);
			}
			
		};
		
		/*
		if(model == null){
			//model = GameObject.FindGameObjectWithTag("MyCube");
			model = GameObject.Find("Cube");
			if(model){
				UnityEngine.Debug.Log("Find it");
			}
		}
		*/
		
		
	}
	
	// Update is called once per frame
	void Update () {
		foreach(GameObject model in models){
			model.transform.Rotate(0, Time.deltaTime*10, 0);
		}
	}
	
	
	
	
}
