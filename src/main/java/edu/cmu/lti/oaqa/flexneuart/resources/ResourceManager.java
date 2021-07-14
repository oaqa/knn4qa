/*
 *  Copyright 2014+ Carnegie Mellon University
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */
package edu.cmu.lti.oaqa.flexneuart.resources;

import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;

import org.apache.commons.io.FilenameUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import edu.cmu.lti.oaqa.flexneuart.apps.CommonParams;
import edu.cmu.lti.oaqa.flexneuart.cand_providers.CandidateProvider;
import edu.cmu.lti.oaqa.flexneuart.cand_providers.LuceneCandidateProvider;
import edu.cmu.lti.oaqa.flexneuart.cand_providers.NmslibKNNCandidateProvider;
import edu.cmu.lti.oaqa.flexneuart.cand_providers.TrecRunCandidateProvider;
import edu.cmu.lti.oaqa.flexneuart.fwdindx.ForwardIndex;
import edu.cmu.lti.oaqa.flexneuart.fwdindx.ForwardIndexBasedFilterAndRecoder;
import edu.cmu.lti.oaqa.flexneuart.giza.GizaTranTableReaderAndRecoder;
import edu.cmu.lti.oaqa.flexneuart.giza.GizaVocabularyReader;
import edu.cmu.lti.oaqa.flexneuart.letor.EmbeddingReaderAndRecoder;


/**
 * This class takes care about loading resources necessary for feature extraction and candidate generation.
 * All resource allocation classes are synchronized on "this" to prevent 
 * race conditions and <b>deadlocks</b>! Fortunately, Java locks are re-entrant
 * to allow for this.
 * 
 * <p>The resource manager accepts an (optional) top-level directory which can be used to
 * address all file-system resources. It does not network resources (TCP/IP addresses
 * of the external extractors and candidate providers). One can always use full resources
 * paths by setting this root directory to null or an empty string.
 * </p>
 * 
 */
public class ResourceManager {
  final static Logger logger = LoggerFactory.getLogger(ResourceManager.class);
  
  public static final String FS = File.separator;
  
  private final String mModel1RootDir;
  private final String mEmbedRootDir;
  private final String mFwdIndexDir;
  private final String mResourceRootDir;
  
  /**
   * Resource manager constructor.
   * 
   * @param resourceRootDir      a top-level directory for file resources (can be null or empty string) : use "."
   *                             to define resources relative to the current directory.
   * @param fwdIndexDir          a directory for forward files (relative to {@link topLevelDir}).
   * @param model1RootDir        a top-level directory for lexical translation files (relative to {@link topLevelDir}).
   * @param embedRootDir         a top-level directory for word embedding files (relative to {@link topLevelDir}).
   */
  public ResourceManager(String resourceRootDir,
                         String fwdIndexDir,
                         String model1RootDir,
                         String embedRootDir) {
    mFwdIndexDir = fwdIndexDir;
    mEmbedRootDir = embedRootDir;
    mModel1RootDir = model1RootDir;
    mResourceRootDir = resourceRootDir !=null ? resourceRootDir : "";
  }
  
  
  
  /**
   * Create an array of candidate providers. If the provider is thread-safe,
   * only one object will be created.
   * 
   * @param resourceManager resource
   * @param provType        provider type
   * @param provURI         provider URI (index location or TCP/IP address)
   * @param configName      configuration file name (can be null)
   * @param threadQty       number of threads
   * 
   * @return  an array of providers or null if the provider type is not recognized
   */
  public CandidateProvider[] createCandProviders(String provType,
                                                        String provURI,
                                                        String configName,
                                                        int threadQty) throws Exception {
    logger.info(String.format("Provider type: %s\n" + 
                              "URI: %s\n" + 
                              "Config file: %s\n" + 
                              "# of threads: %d",
                              provType, provURI, configName != null ? configName : "none", threadQty));
    
    CandidateProvider[] res = new CandidateProvider[threadQty];
    
    JSONKeyValueConfig addConf = null;
    
    if (configName != null) {
      ArrayList<JSONKeyValueConfig> confs = JSONKeyValueConfig.readConfig("Config file, candidate provider: " + provType,
                                                                          FilenameUtils.concat(mResourceRootDir, configName));
      if (confs.size() != 1) {
        throw new Exception("Invalid config: " + configName + ", expect exactly 1 key-value dict, but read: " + confs.size());
      }
      addConf = confs.get(0);
    }
    
    
    if (provType.equalsIgnoreCase(CandidateProvider.CAND_TYPE_LUCENE)) {
      res[0] = new LuceneCandidateProvider(FilenameUtils.concat(mResourceRootDir, provURI), addConf);
      for (int ic = 1; ic < threadQty; ++ic) 
        res[ic] = res[0];
    } else if (provType.equalsIgnoreCase(CandidateProvider.CAND_TYPE_TREC_RUNS)) {
      res[0] = new TrecRunCandidateProvider(FilenameUtils.concat(mResourceRootDir, provURI));
      for (int ic = 1; ic < threadQty; ++ic) {
        res[ic] = res[0];
      }
    } else if (provType.equalsIgnoreCase(CandidateProvider.CAND_TYPE_NMSLIB)) {
      /*
       * NmslibKNNCandidateProvider isn't thread-safe,
       * b/c each instance creates a TCP/IP that isn't supposed to be shared among threads.
       * However, creating one instance of the provider class per thread is totally fine (and is the right way to go). 
       */

      for (int ic = 0; ic < threadQty; ++ic) {
        res[ic] = new NmslibKNNCandidateProvider(provURI, this, addConf);
      }
             
    } else {
      return null;
    }
    
    return res;
  }
  
  
  /**
   * Retrieves and if necessary initializes the forward index:
   * it assumes a standard location and name for forward 
   * 
   * @param fieldName   the name of the field.
   * @return
   * @throws Exception
   */
  public ForwardIndex getFwdIndex(String fieldName) throws Exception {
    if (mFwdIndexDir == null) {
      throw new Exception("There is no forward index directory, likely, you need to specify " + 
          CommonParams.FWDINDEX_PARAM + " in the calling app");
    }
    // Synchronize all resource allocation on the class reference to avoid race conditions AND dead locks
    synchronized (this) {
      if (!mFwdIndices.containsKey(fieldName)) {
        ForwardIndex fwdIndex = ForwardIndex.createReadInstance(fwdIndexFileName(mFwdIndexDir, fieldName));
        mFwdIndices.put(fieldName, fwdIndex);
      }
      return mFwdIndices.get(fieldName);
    }
  }
  
  public EmbeddingReaderAndRecoder getWordEmbed(String fieldName, String fileName) throws Exception {
    if (mEmbedRootDir == null)
      throw new Exception("There is no work embedding root directory, likely, you need to specify " + 
          CommonParams.EMBED_ROOT_DIR_PARAM + " in the calling app");
    // Synchronize all resource allocation on the class reference to avoid race conditions AND dead locks
    synchronized (this) {
      String embedKey = fieldName + "_" + fileName;
      if (!mWordEmbeds.containsKey(embedKey)) {
        ForwardIndex fwdIndx = getFwdIndex(fieldName);
        ForwardIndexBasedFilterAndRecoder filterAndRecoder = new ForwardIndexBasedFilterAndRecoder(fwdIndx);
        mWordEmbeds.put(embedKey, 
            new EmbeddingReaderAndRecoder(FilenameUtils.concat(mResourceRootDir, mEmbedRootDir + FS + fileName), filterAndRecoder));
      }
      return mWordEmbeds.get(embedKey);
    }
  }
  
  public CompositeFeatureExtractor getFeatureExtractor(String configFileName) throws Exception {
    return new CompositeFeatureExtractor(this, FilenameUtils.concat(mResourceRootDir, configFileName));
  }
  
  /**
   * Obtain a translation table.
   * 
   * @param fieldName       an index field name
   * @param model1FilePref  a Model1 file prefix (there are several translation tables in the same root directory).
   * @param flipTranTable   true to flip the translation table
   * @param gizaIterQty     a number of GIZA iterations.
   * @param probSelfTran    a self-translation probability.
   * @param minProb         discard all entries below this threshold.
   * @return
   * @throws Exception
   */
  public Model1Data getModel1Tran(String fieldName, 
                                  String model1FilePref, boolean flipTranTable, 
                                  int gizaIterQty, 
                                  float probSelfTran, float minProb) throws Exception {
    if (mModel1RootDir == null)
      throw new Exception("There is no giza files directory, likely, you need to specify " + 
          CommonParams.MODEL1_ROOT_DIR_PARAM + " in the calling app");
    // Synchronize all resource allocation on the class reference to avoid race conditions AND dead locks
    String key = fieldName + "_" + flipTranTable + "_" + model1FilePref + "_" + gizaIterQty;
    synchronized (this) {
      if (!mModel1Data.containsKey(key)) {
        ForwardIndex fwdIndx = getFwdIndex(fieldName);
        
        ForwardIndexBasedFilterAndRecoder filterAndRecoder = new ForwardIndexBasedFilterAndRecoder(fwdIndx);
        
        
        String prefix = FilenameUtils.concat(mResourceRootDir, mModel1RootDir + FS + model1FilePref + FS);
        GizaVocabularyReader answVoc  = new GizaVocabularyReader(prefix + "source.vcb", filterAndRecoder);
        GizaVocabularyReader questVoc = new GizaVocabularyReader(prefix + "target.vcb", filterAndRecoder);
    
    
        float[] fieldProbTable = fwdIndx.createProbTable(answVoc);
        
    
        GizaTranTableReaderAndRecoder recorder = new GizaTranTableReaderAndRecoder(
                                         flipTranTable,
                                         prefix + "output.t1." + gizaIterQty,
                                         filterAndRecoder,
                                         answVoc, questVoc,
                                         probSelfTran, 
                                         minProb);
        
        mModel1Data.put(key, new Model1Data(recorder, fieldProbTable));
      }
      
      return mModel1Data.get(key);
    }
  }

  private String fwdIndexFileName(String prefixDir, String fieldName) {
    return FilenameUtils.concat(mResourceRootDir, FS + prefixDir + FS + fieldName);
  }  
  
  private HashMap<String, ForwardIndex>               mFwdIndices = new HashMap<String, ForwardIndex>();
  private HashMap<String, EmbeddingReaderAndRecoder>  mWordEmbeds = new HashMap<String, EmbeddingReaderAndRecoder>();
  private HashMap<String, Model1Data>                 mModel1Data = new HashMap<String, Model1Data>();
}
